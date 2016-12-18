import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {Access} from 'lib/access';
import {DialogService} from 'aurelia-dialog';
import {ConfirmDialog} from 'components/confirm-dialog';
import {WSClient} from 'lib/ws-client';
import {EventAggregator} from 'aurelia-event-aggregator';
import {Router} from 'aurelia-router';
import {SourceMove} from './source-move';
import {Configure} from 'lib/config/index';

let logger = LogManager.getLogger('ebooks');

@inject(ApiClient, WSClient, Access, DialogService, EventAggregator, Router, Configure)
export class Ebook {
  ebook
  constructor(client, ws, access, dialog, event, router, config) {
    this.client=client;
    this.ws = ws;
    this.access=access;
    this.dialog =  dialog;
    this.event = event;
    this.router = router;
    this.token = access.token;
    this.canDownload=access.hasRole('user');
    this.canConvert=access.hasRole('user');
    this.conversionFormats = config.get('conversionFormats').map(fmt => {  return {value:fmt, text:fmt}});
    this.subscribeConvertEvents();
  }

  subscribeConvertEvents() {
    let deactivateSource = sourceId => {
      if (this.ebook.sources)
        this.ebook.sources.filter(s => s.id === sourceId)
          .forEach(s => {
            if (s.active) --s.active;
          })
    }
    this.event.subscribe('convert-ready', msg => {
      if (this.ebook && this.ebook.id === msg.data.ebookId) {
      deactivateSource(msg.data.sourceId);
      this.updateConverted();
    }
    });
    this.event.subscribe('convert-error', msg => {
      if (this.ebook && this.ebook.id === msg.data.ebookId) {
      deactivateSource(msg.data.sourceId);
      this.ebook.sources.filter(s => s.id === msg.data.sourceId)
        .forEach(s => s.error = msg.error);
    }
      logger.error('Conversion failed due to '+msg.error);
    })
  }


  get isEditable() {
    return this.ebook && this.access.canEdit(this.ebook.created_by);
  }

  canDeleteSource(source) {
    this.access.canDelete(source.created_by);
  }

  canActivate(params) {
    return this.client.getOne('ebooks', params.id)
      .then(b => {
        this.ebook=b;
        if (b.cover)
          this.coverLoader = this.client.getCover('ebooks', b.id)
        else
          this.coverLoader = null;
        return true;
        })
      .catch(err => {
        logger.error(`Failed to load ${err}`);
        return false;
      });
  }

  activate(params, route) {
    this.updateConverted();
    this.updateShelves();
    route.navModel.setTitle(`Ebook "${this.ebook.title}"`);

  }

  get updateShelves() {
    return () => {
    this.client.getManyUnpaged(`bookshelves/with-ebook/${this.ebook.id}`)
    .then(res => this.shelves = res.items)
    .catch(err => logger.error('Error fetching shelves'));
  }
  }

  updateConverted() {
    this.client.getManyUnpaged(`ebooks/${this.ebook.id}/converted`)
    .then(data => this.convertedSources = data.items)
    .catch(err => logger.error('Cannot get converted sources',err));
  }

  get searchString() {
    let s=''
    if (this.ebook.authors)
      s += this.ebook.authors.slice(0,2).map(a=> a.last_name).join(' ');
    s += ' '+ this.ebook.title;
    return encodeURIComponent(s);
  }

  canDeleteSource(source) {
    return this.access.canDelete(source.created_by);
  }

  canMoveSource(source) {
    return this.access.canEdit(source.created_by);
  }

  deleteSource(source) {
    this.dialog.open({
        viewModel: ConfirmDialog,
        model: {
          action: 'Delete',
          message: `Do you want to delete ${source.format} file from ebook ${this.ebook.title}?`
        }
      })
      .then(resp => {
        if (!resp.wasCancelled) {
        this.removeSource(source, 'Source delete failed:', this.client.delete('sources', source.id));
        }
      });
  }

  removeSource(source, msg, promise) {
    let showError = function(msg, error, errorDetail) {
      logger.error(msg + ' ' + error + ' '+ JSON.stringify(errorDetail));
      alert(msg + ' ' + error);
    }

    promise
    .then(res => {
      if (res.error) {
        showError(msg, res.error, res.error_details);
      } else {
        let idx = this.ebook.sources.findIndex(x => x === source)
        if (idx >= 0) this.ebook.sources.splice(idx, 1);
        this.updateConverted();
      }
    })
    .catch(err => {
      showError('Server error:', err);
    })
  }

  moveSource(source) {
    this.dialog.open({viewModel:SourceMove, model:{ebookId:this.ebook.id, sourceId:source.id}})
    .then(resp=> {
      if (!resp.wasCancelled) {
        logger.debug('Moving to ', resp.output);
        this.removeSource(source, 'Source move failed:',
        this.client.post(`sources/${source.id}/move`, {other_ebook_id: resp.output.id}));
      }
    });
  }

  get convertSource() {
    return (format,source) => {
      source.error=undefined;
      if (format != source.format) {
        this.ws.convertSource(source, format, this.ebook).then(
          taskId => {
            if (! source.active) source.active=1;
            else source.active += 1;
            logger.debug(`Converting ${JSON.stringify(source)} to ${format} in task ${taskId}`);
          })
          .catch(err => {
            source.error=err.toString();
            logger.error('Conversion submission error: '+JSON.stringify(err));
          });
        };
      }
  }

  get enableFormats() {
    let ebook = this;
    return function(item) {
    if (!this.context) return true;
    let converted = ebook.convertedSources && ebook.convertedSources.filter(c => c.source === this.context.id && c.format === item.value).length
    return item.value != this.context.format && ! converted;
  }
  }

  get editActions() {
    return [{text:"Information",value:'edit', icon:'info-circle'}, {text:'Cover', value:'cover', icon:'file-image-o' },
      {text:'Merge', value:'merge', icon:'compress'}];

  }

  get editAction() {
    return action => {
    switch (action) {
      case 'edit':
        this.router.navigateToRoute('ebook-edit', {id:this.ebook.id})
      break;
      case 'cover':
        this.router.navigateToRoute('cover-edit', {id:this.ebook.id})
      break;
      case 'merge':
      this.router.navigateToRoute('ebook-merge', {id: this.ebook.id});
      break;
    }
  }
  }

  get updateRating() {
    return rating => {
      this.client.post(`ebooks/${this.ebook.id}/rate`, {rating})
      .then( res => {
        if (res.error) throw new Error('Rating update error '+ res.error);
        this.ebook.rating = res.rating;
        this.ebook.rating_count = res.rating_count;
      })
    }
  }



}

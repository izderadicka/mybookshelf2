import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {Access} from 'lib/access';
import {DialogService} from 'aurelia-dialog';
import {ConfirmDialog} from 'components/confirm-dialog';
import {WSClient} from 'lib/ws-client';
import {EventAggregator} from 'aurelia-event-aggregator';

let logger = LogManager.getLogger('ebooks');

@inject(ApiClient, WSClient, Access, DialogService, EventAggregator)
export class Ebook {
  ebook
  constructor(client, ws, access, dialog, event ) {
    this.client=client;
    this.ws = ws;
    this.access=access;
    this.dialog =  dialog;
    this.event = event;
    this.token = access.token;
    this.canDownload=access.hasRole('user');
    this.canConvert=access.hasRole('user');
    this.cover = new Image();
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }
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

  canActivate(params) {
    return this.client.getOne('ebooks', params.id)
      .then(b => {
        this.ebook=b;
        if (b.cover)
          this.coverLoader = this.client.getCover('ebooks', b.id);
        return true;
        })
      .catch(err => {
        logger.error(`Failed to load ${err}`);
        return false;
      });
  }

  activate(params) {
    this.updateConverted();
  }

  updateConverted() {
    this.client.getManyUnpaged(`ebooks/${this.ebook.id}/converted`)
    .then(data => this.convertedSources = data.items)
    .catch(err => logger.error('Cannot get converted sources',err));
  }

  attached() {
    if (this.coverLoader)
    this.coverLoader.then (blob => {
      this.cover.src = URL.createObjectURL(blob);
      document.getElementById('cover-holder').appendChild(this.cover);
      })
    .catch(err => {
      logger.warn(`Cannot load cover for ebook ${this.ebook.id}: ${err}`);
    });

  }

  get searchString() {
    let s=''
    if (this.ebook.authors)
      s += this.ebook.authors.slice(0,2).map(a=> a.first_name? a.first_name+' '+a.last_name: a.last_name).join(' ');
    s += ' '+ this.ebook.title;
    return encodeURIComponent(s);
  }

  canDeleteSource(source) {
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
        this.client.delete('sources', source.id)
          .then(res => {
            if (res.error) {
              logger.error('Source delete failed: ' + res.error + ' '+ res.error_details);
              alert('Cannot delete: '+ res.error);
            } else {
              let idx = this.ebook.sources.findIndex(x => x === source)
              if (idx >= 0) this.ebook.sources.splice(idx, 1);
              this.updateConverted();
            }
          })
          .catch(err => {
            logger.error('Server error: ' + err);
          })
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

  get conversionFormats() {
    return [{text:'epub', value:'epub'}, {text:'mobi', value:'mobi'}];
  }

  get enableFormats() {
    let ebook = this;
    return function(item) {
    if (!this.context) return true;
    let converted = ebook.convertedSources && ebook.convertedSources.filter(c => c.source === this.context.id && c.format === item.value).length
    return item.value != this.context.format && ! converted;
  }
  }


}

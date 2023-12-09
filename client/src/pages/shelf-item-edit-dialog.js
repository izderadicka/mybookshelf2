import {LogManager, inject, bindable} from 'aurelia-framework';
import {DialogController} from 'aurelia-dialog';
import {BookshelfItem} from 'models/bookshelf-item';
import {ApiClient} from 'lib/api-client'

let logger = LogManager.getLogger('shelf-edit')

@inject(DialogController, ApiClient, Element)
export class ShelfItemEditDialog {

  constructor(controller, client, elem) {
    this.controller = controller;
    this.elem = elem;
    this.client = client;

  }

  activate(model) {
    this.model=new BookshelfItem(model);
    logger.debug('Dialog activated')
  }

  deactivate() {
    if (this.model) this.model.dispose();
  }

  validate() {
    $('.has-error', this.elem).removeClass('has-error');
    $('.help-block', this.elem).remove();
    let errors = [];

    let addError = function (what,err) {
      errors.push(err);
      let grp=$(`#${what}-input-group`, this.elem);
      grp.addClass('has-error');
      $('<span>').addClass('help-block').text(err).appendTo(grp);

    }
    this.model.validate(addError);
    return errors.length === 0
  }

  save() {
    if (this.validate()) {
      let data = this.model.prepareData();
      if (!Object.keys(data).length) {
        this.error = {
          'error': "No data to save"
        }
      } else {
        this.client.patch('bookshelf-items', data, this.model.id)
          .then(result => {
            if (result.error) {
              this.error = {
                error: "Update error",
                errorDetail: result.error
              };
            } else {
              this.controller.ok();
            }
          })
          .catch(err => this.error = {
            error: 'Server error',
            errorDetail: err
          })

      }
    }
  }
}

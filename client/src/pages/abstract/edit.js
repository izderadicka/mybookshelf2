import {ConfirmDialog} from 'components/confirm-dialog';

export class Edit {
  constructor(client, router, access, dialog) {
    this.client = client;
    this.router = router;
    this.access = access;
    this.dialog = dialog;
    this.afterDeleteRoute = 'welcome';
  }

  canActivate(params) {
    if (params.id !== undefined) {
    return this.client.getOne(this.modelEntity, params.id)
      .then(b => {
        this.model= new this.modelClass(b);
        return this.canEdit(b.created_by);
      })
      .catch(err => { logger.error(`Failed to load ${err}`);
                      return false;})

    } else {
      if (this.canCreateNew) {
        this.model= new this.modelClass();
        return true;
      } else {
      logger.error('Need ID of existing shelf')
      return false;
      }
    }

  }


  deactivate() {
    if (this.model) this.model.dispose();
  }

  validate() {
    $('.has-error').removeClass('has-error');
    $('.help-block').remove();
    let errors = [];

    let addError = function (what,err) {
      errors.push(err);
      let grp=$(`#${what}-input-group`);
      grp.addClass('has-error');
      $('<span>').addClass('help-block').text(err).appendTo(grp);

    }
    this.model.validate(addError);
    return errors.length === 0
  }

  save() {
    this.error=undefined;

    if (this.validate()) {
      let data = this.model.prepareData();
      if (!data || ! Object.keys(data).length) {
        this.error={error:'No changes to save'};
        return
      }
      let result;
      if (this.model.id) {
        result = this.client.patch(this.modelEntity, data, this.model.id)
      } else {
        result = this.client.post(this.modelEntity, data);
      }

      result.then(res => {
        if (res.error) {
          this.error={error:res.error, errorDetail:res.error_details}
        } else if (res.id) {
          this.doAfterSave(res.id)
          .then(() => {
            this.router.navigateToRoute(this.viewRoute, {id:res.id});
          })
          .catch(err => this.error = {error:'After Save action error', errorDetail: err});
        } else {
          this.error = {error:'Invalid respose', errorDetail: 'Entity ID is missing'}
        }
      })
      .catch(err => this.error={error:'Request failed', errorDetail:err})


    } else {
      logger.debug(`Validation fails`)
    }
  }

  doAfterSave() {
    return Promise.resolve()
  }


  cancel() {
    if (this.model.id) {
      this.router.navigateToRoute(this.viewRoute, {id:this.model.id});
    } else {
      this.router.navigate(this.afterDeleteRoute);
    }
  }

  canDelete() {
    return this.model.id && this.access.canDelete(this.model.created_by);
  }

  canEdit() {
    return this.model.id && this.access.canEdit(this.model.created_by);
  }

  delete() {
    this.error=undefined;
    this.dialog.open({viewModel:ConfirmDialog, model: {action:'Delete', message:this.deleteConfirmMessage}})
    .then(response => {
      if (!response.wasCancelled && this.model.id) {
        this.client.delete(this.modelEntity, this.model.id)
        .then(res => {
          if (res.error) {
            this.error={error:res.error, errorDetail:res.error_details}
          } else {
            this.router.navigateToRoute(this.afterDeleteRoute);
          }
        })
        .catch(err=> this.error={error:'Delete error', errorDetail:err})

      }
    });
  }

  get deleteConfirmMessage() {
    return 'Do you want to delete this?';
  }
}

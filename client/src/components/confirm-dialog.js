import {inject} from "aurelia-framework";
import {DialogController} from "aurelia-dialog";


@inject(DialogController)
export class ConfirmDialog {
  constructor(controller) {
    this.controller=controller;
  }

  activate(model) {
    this.action = model.action;
    this.message = model.message;
  }
}

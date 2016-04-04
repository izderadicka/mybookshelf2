import {bindable, computedFrom, customElement} from 'aurelia-framework'

@customElement('author')
export class Author {
  @bindable author
  @bindable last=true

  @computedFrom('author')
  get link(){

    return '#/author/'+(this.author.firstname?`${this.author.lastname}/${this.author.firstname}`:this.author.lastname);
  }

  @computedFrom('author')
  get fullName() {
    return this.author.firstname?`${this.author.firstname} ${this.author.lastname}`:this.author.lastname;
  }
}

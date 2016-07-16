import {bindable, computedFrom, customElement} from 'aurelia-framework'

@customElement('author')
export class Author {
  @bindable author;
  @bindable last=true;
  @bindable linked = true;

  @computedFrom('author')
  get link(){

    return '#/author/'+this.author.id;
  }

  @computedFrom('author')
  get fullName() {
    return this.author.first_name?`${this.author.first_name} ${this.author.last_name}`:this.author.last_name;
  }
}

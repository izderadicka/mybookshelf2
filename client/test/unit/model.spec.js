import {
  Ebook
} from 'models/ebook';

import {Bookshelf} from 'models/bookshelf';
import {BookshelfItem} from 'models/bookshelf-item';

let c = new Container();
c.makeGlobal();

import {
  Container
} from 'aurelia-dependency-injection';


describe("When using Ebook model", () => {
  let ebookMin = {
    title: 'Nejaka sragoora',
    language: {
      id: 1
    }
  };

  let errorHandler;
  beforeEach(() => {
    errorHandler = {
      addError(item, error) {}
    };
    spyOn(errorHandler, 'addError');
  });

  it('can create valid minimal ebook', () => {
    let ebook = new Ebook(ebookMin);
    expect(ebook.title).toBe('Nejaka sragoora');
    expect(ebook.language.id).toBe(1);
    expect(ebook.isNew()).toBeTruthy();
    ebook.validate(errorHandler.addError);
    expect(errorHandler.addError).not.toHaveBeenCalled();
    let data = ebook.prepareData();
    expect(data.title).toBe('Nejaka sragoora');
    expect(data.language.id).toBe(1);
  });

  it('can track changes', (done) => {
    let ebook = new Ebook(Object.assign(ebookMin, {
      id: 1,
      version_id: 1
    }));
    let data = ebook.prepareData();

    expect(ebook.isNew()).toBeFalsy();
    expect(Object.keys(data).length).toBe(0);
    ebook.title = 'Slusny';
    //console.log(ebook);
    // need to set as new task because observers updates are happening after this task
    setTimeout(() => {
      data = ebook.prepareData();
      expect(ebook.hasChanged('title')).toBeTruthy();
      expect(ebook.hasChanged('series')).toBeFalsy();
      expect(Object.keys(data).length).toBe(3);
      expect(data.title).toBe('Slusny');
      done();
    });
  });

  it('validates data ', (done) => {
    let ebook = new Ebook({});
    let addError = errorHandler.addError;
    ebook.validate(addError);
    expect(addError).toHaveBeenCalledTimes(2);
    expect(addError.calls.argsFor(0)[0]).toBe('title');
    expect(addError.calls.argsFor(1)[0]).toBe('language');
    ebook.series_index =  1;
    ebook.title = 'Hey';
    ebook.language = {id:1};
    setTimeout(() => {
      ebook.validate(addError);
      expect(addError).toHaveBeenCalledTimes(3);
      expect(addError.calls.argsFor(2)[0]).toBe('series');
      done();
    })
  });

  it('track changes in collections', (done) => {
    let ebook = new Ebook(Object.assign(ebookMin, {authors: [{first_name: 'Jan', last_name: 'Sebran'}]}));
    ebook.authors.push({first_name: 'Josef', last_name:'Usak'});
    setTimeout(() => {
        ebook.validate(errorHandler.addError);
        expect(errorHandler.addError).not.toHaveBeenCalled();
        expect(ebook.hasChanged('authors')).toBeTruthy();
        expect(ebook.authors.length).toBe(2);
        done()
    })

  });
});

  describe("When using other models", () => {
    let errorHandler;
    beforeEach(() => {
      errorHandler = {
        addError(item, error) {}
      };
      spyOn(errorHandler, 'addError');
    });


  it('Bookshelf model works', (done) => {
    let shelf= new Bookshelf({name:'test'});
    shelf.validate(errorHandler.addError);
    expect(errorHandler.addError).not.toHaveBeenCalled();
    shelf.name = 'abc'.repeat(100);
    setTimeout(() => {
      expect(shelf.hasChanged('name')).toBeTruthy();
      shelf.validate(errorHandler.addError);
      expect(errorHandler.addError).toHaveBeenCalled();
      expect(errorHandler.addError.calls.argsFor(0)[0]).toBe('name');
      done();
    })
  });

  it('BookshelfItem model works', (done) => {
    let item = new BookshelfItem({ebook:{id:1}, order:1});
    item.validate(errorHandler.addError);
    expect(errorHandler.addError).not.toHaveBeenCalled();
    item.series = {id:1};
    setTimeout(() => {
      expect(item.hasChanged('series')).toBeTruthy();
      item.validate(errorHandler.addError);
      expect(errorHandler.addError).toHaveBeenCalled();
      expect(errorHandler.addError.calls.argsFor(0)[0]).toBe('item');
      done();
    })

  });


});

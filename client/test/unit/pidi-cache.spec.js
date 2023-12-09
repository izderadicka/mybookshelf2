
import {PidiCache} from 'lib/pidi-cache';


describe('When using pidi cache', () => {
  let c;
  beforeEach(() => {
    c = new PidiCache(0.5)
  })
it('Stores gets, and clears', () => {
  c.add('ebooks', {id:123, title:'Hey How'});
  let e = c.get('ebooks', 123);
  expect(e.title).toBe('Hey How');
  expect(c.get('ebooks', 234)).toBeUndefined();
  c.clear('ebooks');
  expect(c.get('ebooks', 123)).toBeUndefined();

})

it('Expires old values', (done) => {
  c.add('ebooks', {id:123, title:'Hey How'});
  let e = c.get('ebooks', 123);
  expect(e.title).toBe('Hey How');
  setTimeout(() => {
    expect(c.get('ebooks', 123)).toBeUndefined();
    done();
  }, 600)
})

})

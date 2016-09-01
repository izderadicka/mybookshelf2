export const ROUTES =
[{
    route: ['', 'welcome'],
    name: 'welcome',
    moduleId: 'pages/welcome',
    title: 'Welcome'
  }, {
    route: 'ebooks',
    name: 'ebooks',
    moduleId: 'pages/ebooks',
    nav: true,
    title: 'Ebooks',
    auth: true
  }, {
    route: 'login',
    name: 'login',
    moduleId: 'pages/login',
    title: 'Login'
  }, {
    route: 'ebook/:id',
    name: 'ebook',
    moduleId: 'pages/ebook',
    title: 'Ebook',
    auth: true
  }, {
    route: 'search/:query',
    name: 'search',
    moduleId: 'pages/search',
    title: 'Search Results',
    auth: true
  }, {
    route: ['author/:id'],
    name: 'author',
    moduleId: 'pages/author',
    title: 'Authors books',
    auth: true
  }, {
    route: 'upload',
    name: 'upload',
    moduleId: 'pages/upload',
    title: 'Upload Ebook',
    nav: true,
    auth: true
  },
  {
    route: 'upload-result/:id',
    name : 'upload-result',
    moduleId: 'pages/upload-result',
    title: 'Upload results',
    auth: true
  },

  {
    route: 'ebook-edit/:id',
    name: 'ebook-edit',
    moduleId: 'pages/ebook-edit',
    title: 'Edit Ebook',
    auth: true
  },
  {
    route: 'ebook-create',
    name: 'ebook-create',
    moduleId: 'pages/ebook-edit',
    title: 'Create Ebook',
    auth: true
  },

// testing routes
  {
    route: 'test',
    name : 'test',
    moduleId: 'test/test-page',
    title: 'Just testing'
  },


];

export const ROUTES =
[{
    route: ['', 'welcome'],
    name: 'welcome',
    moduleId: 'pages/welcome',
    title: 'Welcome',
    auth: true
  }, {
    route: 'ebooks',
    name: 'ebooks',
    moduleId: 'pages/ebooks',
    nav: 1,
    title: 'Ebooks',
    auth: true
  }, {
    route: 'shelves',
    name: 'shelves',
    moduleId: 'pages/shelves',
    nav: 2,
    title: 'Bookshelves',
    auth: true
  },
  {
    route: 'shelf/:id',
    name: 'shelf',
    moduleId: 'pages/shelf',
    title: 'Bookshelf',
    auth: true
  },
  {
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
    route: ['series/:id'],
    name: 'series',
    moduleId: 'pages/series',
    title: 'Books in series',
    auth: true
  }, {
    route: 'upload',
    name: 'upload',
    moduleId: 'pages/upload',
    title: 'Upload',
    nav: 3,
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
    route: 'ebook-merge/:id',
    name: 'ebook-merge',
    moduleId: 'pages/ebook-merge',
    title: 'Merge Ebook',
    auth: true
  },
  {
    route: 'cover-edit/:id',
    name: 'cover-edit',
    moduleId: 'pages/cover-edit',
    title: 'Edit Cover',
    auth: true
  },
  {
    route: 'ebook-create',
    name: 'ebook-create',
    moduleId: 'pages/ebook-edit',
    title: 'Create Ebook',
    auth: true
  },
  {
    route: 'shelf/add/:what/:id',
    name: 'add-to-shelf',
    moduleId: 'pages/ebook-add-to-shelf',
    title: 'Add To Bookshelf',
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

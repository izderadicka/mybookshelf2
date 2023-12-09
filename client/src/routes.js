export const ROUTES =
[{
    route: ['', 'welcome'],
    name: 'welcome',
    moduleId: 'pages/welcome',
    title: 'Welcome',
    auth: true
  },
  {
    route: 'user',
    name: 'user',
    moduleId: 'pages/profile',
    title: 'User Profile',
    auth: true
  },
  {
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
   route: 'upload',
   name: 'upload',
   moduleId: 'pages/upload',
   title: 'Upload',
   nav: 3,
   auth: true
  },
  {
    route: 'conversions',
    name: 'conversions',
    moduleId: 'pages/conversions',
    title: 'Conversions',
    nav: 4,
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
    route: 'shelf-edit/:id',
    name: 'shelf-edit',
    moduleId: 'pages/shelf-edit',
    title: 'Edit Bookshelf Information',
    auth: true
  },
  {
    route: 'shelf-merge/:id',
    name: 'shelf-merge',
    moduleId: 'pages/shelf-merge',
    title: 'Merge Bookshelfs',
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
  },
  {
    route: ['author-edit/:id'],
    name: 'author-edit',
    moduleId: 'pages/author-edit',
    title: 'Edit Author',
    auth: true
  },
  {
    route: ['author-merge/:id'],
    name: 'author-merge',
    moduleId: 'pages/author-merge',
    title: 'Merge Authors',
    auth: true
  },
  {
    route: ['series/:id'],
    name: 'series',
    moduleId: 'pages/series',
    title: 'Books in series',
    auth: true
  }, {
    route: ['series-edit/:id'],
    name: 'series-edit',
    moduleId: 'pages/series-edit',
    title: 'Edit Series',
    auth: true
  },
  {
    route: ['series-merge/:id'],
    name: 'series-merge',
    moduleId: 'pages/series-merge',
    title: 'Merge Series',
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
    title: 'Merge Ebooks',
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
    route: 'ebook/:ebookId/source/:sourceId/move',
    name: 'source-move',
    moduleId: 'pages/source-move',
    title: 'Move Source to Other Ebook',
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

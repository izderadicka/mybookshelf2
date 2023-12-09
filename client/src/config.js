var config = {
  "version":"0.1",
  "debug": true,
  "api": {
    "protocol": "",
    "host":"",
    "port": null,
    "path": "/api"
  },
  "backend-ws": {
    "host":"",
    "port": null
  },
  "maxUploadSize": 104857600,
  "notificationAttentionTimeout": 20,
  "locale": undefined,
  "conversionFormats": ['epub', 'mobi']
}

var authConfig = {
    loginUrl: '/login',
    providers: {
        google: {
            clientId: '239531826023-ibk10mb9p7ull54j55a61og5lvnjrff6.apps.googleusercontent.com'
        }
        ,
        linkedin:{
            clientId:'778mif8zyqbei7'
        },
        facebook:{
            clientId:'1452782111708498'
        }
    }
};

config.authentication = authConfig;

export default config;

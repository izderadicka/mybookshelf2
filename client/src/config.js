var config = {
  "version":"0.1",
  "debug": true,
  "api": {
    "protocol": "",
    "host":"",
    "port": 6006,
    "path": "/api"
  },
  "wamp": {
    "host":"",
    "port": 8080,
    "path": "/ws",
    "realm": "realm1"
  },
  "maxUploadSize": 104857600,
  "notificationAttentionTimeout": 20
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

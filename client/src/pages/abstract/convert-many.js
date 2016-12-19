import {LogManager} from 'aurelia-framework';

const logger = LogManager.getLogger('convert-many');

export class ConvertMany {
  constructor(access, config, wsClient) {
    this.wsClient = wsClient;
    this.conversionFormats = config.get('conversionFormats').map(fmt => {  return {value:fmt, text:fmt}});
    this.canConvertMany=access.hasRole('user');
  }

  get convertMany() {
    return fmt => {
      this.wsClient.convertMany(this.entity, this[this.entity], fmt)
      .then(taskId => {
        logger.debug('Conversion started as task id#' + taskId);
      })
      .catch(err => {
        logger.error(`Conversion failed with ${err}`);
      })

    }
  }
}

let sufixes = ['B', 'kB', 'MB', 'GB', 'TB']

export class SizeValueConverter {

  toView(val) {
    let index = 0;
    while (val >=1024 && index < sufixes.length) {
      val = val/1024;
      index++;
    }
    return `${Math.round(val*10)/10} ${sufixes[index]}`;
  }
}

export class SliceValueConverter {
  toView(value, start, end) {
    return value.slice(start, end)
  }
}

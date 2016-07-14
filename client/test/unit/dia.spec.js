import diacritic from 'diacritic';

describe('When using diacritic remove', () => {
  it('should remove diacritics marks form text', () => {
    let testString = 'ěščřžýáíéúůďťň';
    expect(diacritic.clean(testString)).toBeDefined();
    expect(diacritic.clean(testString)).toEqual('escrzyaieuudtn');
  }
)
})

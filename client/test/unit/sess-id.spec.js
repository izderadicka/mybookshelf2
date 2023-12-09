import {randomSessionId} from 'lib/ws-client';

describe("When generating session id", () => {
    it("generates 32 hexa chars by default", () => {
        let s = randomSessionId();
        expect(s.length).toBe(32);
    });

    it("generates different values", () => {
        let s1 =  randomSessionId();
        let s2 =  randomSessionId();
        expect(s1.length).toBe(s2.length);
        expect(s1==s2).toBeFalsy();
    })
})
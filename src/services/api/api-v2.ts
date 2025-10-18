import {API} from "./";
import {createAxiosInstanceV2} from "./.conf";

const api = createAxiosInstanceV2()

// Обрабатывает success / data / message
export class APIv2 extends API {
  constructor(URL: string) {
    super(URL, api);
  }
}
import {type AxiosInstance, type AxiosRequestConfig} from 'axios'
import {createAxiosInstance} from "./.conf";

export type AxiosConfig = AxiosRequestConfig & {
  methodName?: string
  subId?: string
  id?: string
}


const api = createAxiosInstance()
const controllersDict: Record<string, AbortController|undefined> = {}; // Хранение AbortController для активных запросов

export class API {

  constructor(private URL: string, private _api: AxiosInstance = api) {}

  private _url(conf?: AxiosConfig) {
    let _url = this.URL
    if(conf) {
      if(conf.subId) {
        _url += `/${conf.subId}`
      }
      if(conf.methodName) {
        _url += `/${conf.methodName}`
      }
      if(conf.id) {
        _url += `/${conf.id}`
      }
    }
    return _url
  }

  private async exec<T>(method: string, data?: any, conf?: AxiosConfig) {

    const url = this._url(conf)

    controllersDict[url]?.abort(); // Отменяем предыдущий запрос

    const controller = new AbortController();
    // Сохраняем контроллер в объект
    controllersDict[url] = controller;

    const response = await this._api.request<T, T>({
      url: this._url(conf),
      method,
      data,
      signal: controller.signal,
      ...conf,
    })

    delete controllersDict[url]

    return response
  }

  get<T = unknown>(conf?: AxiosConfig) {
    return this.exec<T>('GET', undefined, conf)
  }

  post<T = unknown>(data?: any, conf?: AxiosConfig) {
    return this.exec<T>('POST', data, conf)
  }

  put<T = unknown>(data?: any, conf?: AxiosConfig) {
    return this.exec<T>('PUT', data, conf)
  }

  delete<T = unknown>(conf?: AxiosConfig) {
    return this.exec<T>('DELETE', undefined, conf)
  }

  options<T = unknown>(conf?: AxiosConfig) {
    return this.exec<T>('OPTIONS', undefined, conf)
  }

  // FormData {file:file}
  upload<F extends Blob>(file: F, conf?: AxiosConfig) {
    const form = new FormData()
    form.append('file', file)
    return this.post<void>(form, conf);
  }

  download(conf?: AxiosConfig) {
    return this.post<Blob>({}, {
      responseType: 'blob',
      ...conf
    });
  }
}
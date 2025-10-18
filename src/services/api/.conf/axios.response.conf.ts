import axios, { type AxiosResponse, type AxiosInstance } from 'axios'

function checkJson(data: string) {
  let json = null

  try {
    json = JSON.parse(data)
  } catch(e) {}

  if(json && json.success == false)
    throw new Error(json.message)
}

function debugResponse(response: AxiosResponse) {
  console.debug('===============================')
  console.debug(response.config.url)
  try {console.debug(JSON.parse(response.config.data))}
  catch (e) {}
  console.debug(response)
}

const ResponseConfig = {
  onFulFilled(response: AxiosResponse) {
    debugResponse(response)
    return response.data
  },
  async onFulFilledV2(response: AxiosResponse) {
    debugResponse(response)

    const d = response.data

    if(d instanceof Blob) {
      if(d.type == 'application/json') {
        const json = await response.data.text()
        checkJson(json)
      }
      return d
    }
    else {
      if(d.success)
        return d.data
      else
        throw new Error(d.message)
    }
  },
  onRejected(error: unknown) {
    console.error(error)

    if(axios.isAxiosError(error) && error.status === 400) {
      return Promise.reject(error.response?.data || error);
    }

    return Promise.reject(error);
  }
}

export function setAxiosResponseConfig(axiosInstance: AxiosInstance) {
  // Глобальные обработчики запросов (для логирования)
  axiosInstance.interceptors.response.use(ResponseConfig.onFulFilled, ResponseConfig.onRejected);
}

export function setAxiosResponseConfigV2(axiosInstance: AxiosInstance) {
  // Глобальные обработчики запросов (для логирования)
  axiosInstance.interceptors.response.use(ResponseConfig.onFulFilledV2, ResponseConfig.onRejected);
}

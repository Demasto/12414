import axiosRetry from "axios-retry";
import {Axios, AxiosError, type AxiosInstance} from "axios";

export function setAxiosRetryConfig(axiosInstance: AxiosInstance) {
  axiosRetry(axiosInstance, {
    retries: 1,  // Количество попыток
    retryDelay: (retryCount) => { return retryCount * 1000 }, // Время между попытками в миллисекундах
    retryCondition: (error) => {
      return error.code == AxiosError.ECONNABORTED || error.code == AxiosError.ERR_NETWORK ||  error.status == 408  // Повторять только при разрыве соединения
    },
    shouldResetTimeout: true,
    onRetry: (retryCount, error, requestConfig) => {
      console.error(retryCount);
      console.error(error);
      console.error(requestConfig);
    }
  })
}

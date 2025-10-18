import type { AxiosRequestConfig } from "axios";

interface BaseConfig extends AxiosRequestConfig {
  baseURL: string,
  timeout: number
}

export const axiosConfig : BaseConfig = {
  baseURL: '/api',
  timeout: 10000,
}
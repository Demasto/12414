import axios from "axios";
import {axiosConfig} from "./axios.conf";
import {setAxiosResponseConfig, setAxiosResponseConfigV2} from "./axios.response.conf";
import {setAxiosRetryConfig} from "./axios.retry.conf";


export function createAxiosInstance() {
    const axiosInstance = axios.create(axiosConfig)
    setAxiosResponseConfig(axiosInstance)
    setAxiosRetryConfig(axiosInstance)
    return axiosInstance
}

export function createAxiosInstanceV2() {
    const axiosInstance = axios.create(axiosConfig)
    setAxiosResponseConfigV2(axiosInstance)
    setAxiosRetryConfig(axiosInstance)
    return axiosInstance
}
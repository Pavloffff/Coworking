import axios, { AxiosInstance } from 'axios'
import { config } from '../config/config'

const serversConfiguratorApiClient: AxiosInstance = axios.create({
	baseURL: config.servers_configurator_api.baseUrl,
	timeout: config.servers_configurator_api.timeout,
	headers: {
		'Content-Type': 'application/json',
	},
})

export default serversConfiguratorApiClient

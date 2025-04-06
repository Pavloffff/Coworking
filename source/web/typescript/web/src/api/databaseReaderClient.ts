import axios, { AxiosInstance } from 'axios'
import { config } from '../config/config'

const databaseReaderApiClient: AxiosInstance = axios.create({
	baseURL: config.database_reader_api.baseUrl,
	timeout: config.database_reader_api.timeout,
	headers: {
		'Content-Type': 'application/json',
	},
})

export default databaseReaderApiClient

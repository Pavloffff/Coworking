interface AppConfig {
	database_reader_api: {
		baseUrl: string
		timeout: number
	}
	servers_configurator_api: {
		baseUrl: string
		timeout: number
	}
}

export const config: AppConfig = {
	database_reader_api: {
		baseUrl:
			import.meta.env.VITE_DATABASE_READER_API_BASE_URL ||
			'http://localhost:8001/api/v1',
		timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 5000,
	},
	servers_configurator_api: {
		baseUrl:
			import.meta.env.VITE_SERVERS_CONFIGURATOR_API_BASE_URL ||
			'http://localhost:8000/api/v1',
		timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 5000,
	},
}

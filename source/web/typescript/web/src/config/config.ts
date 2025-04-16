interface AppConfig {
	database_reader_api: {
		baseUrl: string
		timeout: number
	}
	servers_configurator_api: {
		baseUrl: string
		timeout: number
	}
	notifications_pisher_ws_endpoint: string
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
	notifications_pisher_ws_endpoint: `${
		import.meta.env.VITE_NOTIFICATIONS_PUSHER_API_BASE_URL ||
		'ws://localhost:8002/api/v1'
	}/notifications`,
}

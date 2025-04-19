import VoiceDevicesLogoPanel from '../components/panels/VoiceDevicesLogoPanel'
import InputPanel from '../components/panels/InputPanel'
import ProjectHeader from '../components/headers/ProjectHeader'
import ItemsPanel from '../components/panels/ItemsPanel'
import ChatPanel from '../components/panels/ChatPanel'
import { config } from '../config/config'
import { v4 as uuidv4 } from 'uuid'
import useWebSocket from 'react-use-websocket'
import { useCallback, useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { serversApi } from '../api/servers/serversApi'
import Cookies from 'js-cookie'
import { ServerModel } from '../api/types'
import { useNavigate } from 'react-router-dom'

const chatData = [
	{
		name: 'Иван Иванов',
		text: 'Привет! Как дела?',
	},
	{
		name: 'Мария Петрова',
		text: 'Привет! Пока не родила!',
	},
	{
		name: 'Пидр Сидоров',
		text: 'Как продвигается проект?',
	},
	{
		name: 'Анна Кузнецова',
		text: 'Мы почти готовы!',
	},
	{
		name: 'Иван Иванов',
		text: 'Привет! Как дела?',
	},
	{
		name: 'Мария Петрова',
		text: 'Привет! Пока не родила!',
	},
	{
		name: 'Пидр Сидоров',
		text: 'Как продвигается проект?',
	},
	{
		name: 'Анна Кузнецова',
		text: 'Мы почти готовы!',
	},
]

// const mockServers = [
// 	{
// 		server_id: '1',
// 		owner_id: 'user1',
// 		name: 'Dungeon',
// 		// avatar_url: '',
// 		// 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/Sintel.jpg',
// 	},
// 	{
// 		server_id: '2',
// 		owner_id: 'user1',
// 		name: 'Mangeon',
// 		// avatar_url:
// 		// 	'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/Sintel.jpg',
// 	},
// 	{
// 		server_id: '3',
// 		owner_id: 'user2',
// 		name: 'Вихорьково main',
// 	},
// ]
// const useServers = () => {
// 	const access_token = Cookies.get('access_token') as string
// 	const refresh_token = Cookies.get('refresh_token') as string
// 	const socketUrl = `${
// 		config.notifications_pisher_ws_endpoint
// 	}/${uuidv4()}?token=${access_token}`
// 	console.log(socketUrl)

// 	const { data, refetch } = useQuery<ServerModel[]>({
// 		queryKey: ['getUserServers'],
// 		queryFn: async () => {
// 			const response = await serversApi.getUserServers(
// 				access_token,
// 				refresh_token
// 			)
// 			return response.data
// 		},
// 	})

// 	const { lastMessage } = useWebSocket(socketUrl)
// 	useEffect(() => {
// 		if (lastMessage !== null) {
// 			refetch()
// 		}
// 	}, [lastMessage, refetch])
// 	return data
// }

const Main = () => {
	const navigate = useNavigate()
	const access_token = Cookies.get('access_token') as string
	const refresh_token = Cookies.get('refresh_token') as string

	const isMounted = useRef(false) // Добавляем реф для отслеживания монтирования
	const wsUrl = useRef<string>('')

	const [selectedServerId, setSelectedServerId] = useState<string | null>(null)
	const handleServerSelect = useCallback((serverId: string) => {
		setSelectedServerId(serverId)
		Cookies.set('selected_server', serverId)
		console.log('Selected server:', serverId)
	}, [])

	const handleLogout = useCallback(() => {
		//TODO: обратно
		// Cookies.remove('access_token')
		// Cookies.remove('refresh_token')
		// navigate('/login')
		navigate('/')
	}, [navigate])

	const { data: servers, refetch } = useQuery<ServerModel[]>({
		queryKey: ['servers'],
		queryFn: async (): Promise<ServerModel[]> => {
			try {
				const response = await serversApi.getUserServers(
					access_token,
					refresh_token
				)
				return response.data
			} catch (error) {
				console.log(error)

				handleLogout()
				return []
			}
		},
		refetchOnWindowFocus: false, // Отключаем обновление при фокусе окна
		refetchOnMount: false, // Отключаем обновление при монтировании
		refetchOnReconnect: false, // Отключаем обновление при реконнекте
		staleTime: Infinity, // Данные никогда не считаются устаревшими
		retry: false,
		enabled: !!access_token,
	})

	const { lastMessage } = useWebSocket(wsUrl.current, {
		shouldReconnect: () => false,
		onError: (event: Event) => {
			console.error('WebSocket error:', event)
			handleLogout()
		},
		onClose: (event: CloseEvent) => {
			if (event.code !== 1000) handleLogout()
		},
		reconnectAttempts: 0,
	})

	// Обновление данных при новых сообщениях
	useEffect(() => {
		if (access_token && !wsUrl.current) {
			wsUrl.current = `${
				config.notifications_pisher_ws_endpoint
			}/${uuidv4()}?token=${access_token}`
		}
	}, [access_token])

	// Обновление данных при новых сообщениях
	useEffect(() => {
		if (isMounted.current && lastMessage) {
			refetch().then(() => {
				const currentServer = servers?.find(
					s => s.server_id === selectedServerId
				)
				if (!currentServer && servers && servers.length > 0) {
					const firstId = servers[0].server_id
					setSelectedServerId(firstId)
					Cookies.set('selected_server', firstId)
				}
			})
		}
	}, [lastMessage, refetch, selectedServerId, servers])

	// Отслеживаем монтирование компонента
	useEffect(() => {
		isMounted.current = true
		return () => {
			isMounted.current = false
		}
	}, [])

	useEffect(() => {
		if (servers && servers.length > 0) {
			const savedServerId = Cookies.get('selected_server')
			const serverExists = servers.some(s => s.server_id === savedServerId)

			if (savedServerId && serverExists) {
				setSelectedServerId(savedServerId)
			} else {
				const firstId = servers[0].server_id
				setSelectedServerId(firstId)
				Cookies.set('selected_server', firstId)
				console.log('Default server selected:', firstId)
			}
		}
	}, [servers])

	return (
		<div
			style={{
				position: 'absolute',
				top: 0,
				left: 0,
				right: 0,
				bottom: 0,
				overflow: 'hidden',
				backgroundColor: '#fff',
			}}
		>
			<div
				style={{
					display: 'flex',
					flexDirection: 'column',
					width: '100%',
					height: '100%',
					padding: '16px',
					boxSizing: 'border-box',
				}}
			>
				<div
					style={{
						flex: 1,
						display: 'flex',
						marginBottom: '16px',
						minHeight: 0,
						marginRight: '28px',
					}}
				>
					<div
						style={{
							flex: '0 0 25%',
							paddingRight: '16px',
							overflow: 'auto',
							marginRight: '16px',
							minHeight: 0,
						}}
					>
						<ItemsPanel
							servers={servers}
							onServerSelect={handleServerSelect}
							selectedServerId={selectedServerId}
						/>
					</div>
					<div
						style={{
							flex: '0 0 75%',
							display: 'flex',
							flexDirection: 'column',
							overflow: 'hidden',
							minHeight: 0,
						}}
					>
						<div
							style={{
								flexShrink: 0,
								marginBottom: '16px',
							}}
						>
							<ProjectHeader projectName="Dungeon" itemName="чат Пивальди" />
						</div>
						<div
							style={{
								flex: 1,
								overflowY: 'auto',
								marginRight: '16px',
								minHeight: 0,
							}}
						>
							<ChatPanel chatData={chatData} />
						</div>
					</div>
				</div>
				<div style={{ flexShrink: 0, display: 'flex', marginRight: '28px' }}>
					<div
						style={{
							flex: '0 0 25%',
							paddingRight: '16px',
							overflow: 'auto',
							marginRight: '16px',
							minHeight: 0,
						}}
					>
						<VoiceDevicesLogoPanel />
					</div>
					<div
						style={{
							flex: '0 0 75%',
							overflow: 'auto',
							minHeight: 0,
						}}
					>
						<InputPanel />
					</div>
				</div>
			</div>
		</div>
	)
}

export default Main

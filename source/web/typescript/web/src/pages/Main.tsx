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
import { ChatItemScheme, ServerModel, TextChannelModel } from '../api/types'
import { useNavigate } from 'react-router-dom'
import { textChannelsApi } from '../api/textChannels/textChannelsApi'
import { chatItemsApi } from '../api/chatItems/chatItemsApi'

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

	const [selectedTextChannelId, setSelectedTextChannelId] = useState<
		string | null
	>(null)
	const handleTextChannelSelect = useCallback((textChannelId: string) => {
		setSelectedTextChannelId(textChannelId)
		Cookies.set('selected_text_channel', textChannelId)
		console.log('Selected text channel:', textChannelId)
	}, [])

	const handleLogout = useCallback(() => {
		//TODO: обратно вернуть логику
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

	const { data: textChannels, refetch: refetchChannels } = useQuery<
		TextChannelModel[]
	>({
		queryKey: ['textChannels', selectedServerId],
		queryFn: async () => {
			if (!selectedServerId) return []
			const response = await textChannelsApi.getServerTextChannels(
				parseInt(selectedServerId),
				access_token,
				refresh_token
			)
			return response.data
		},
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		staleTime: Infinity,
		retry: false,
		enabled: !!selectedServerId,
	})

	const { data: currentServer } = useQuery({
		queryKey: ['currentServer', selectedServerId],
		queryFn: async () => {
			if (!selectedServerId) return null
			const response = await serversApi.getCurrentServer(
				parseInt(selectedServerId),
				access_token,
				refresh_token
			)
			return response.data
		},
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		staleTime: Infinity,
		retry: false,
		enabled: !!selectedServerId,
	})

	const { data: currentTextChannel } = useQuery({
		queryKey: ['currentTextChannel', selectedTextChannelId],
		queryFn: async () => {
			if (!selectedTextChannelId) return null
			const response = await textChannelsApi.getCurrentTextChannel(
				parseInt(selectedTextChannelId),
				access_token,
				refresh_token
			)
			return response.data
		},
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		staleTime: Infinity,
		retry: false,
		enabled: !!selectedServerId,
	})

	const { data: chatItems, refetch: refetchChat } = useQuery<ChatItemScheme[]>({
		queryKey: ['chatItems', selectedTextChannelId],
		queryFn: async () => {
			if (!selectedTextChannelId) return []
			const response = await chatItemsApi.getTextChannelsChatItems(
				parseInt(selectedTextChannelId),
				access_token,
				refresh_token
			)
			return response.data
		},
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		staleTime: Infinity,
		retry: false,
		enabled: !!selectedTextChannelId,
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
				const currentServerModel = servers?.find(
					s => s.server_id === selectedServerId
				)
				if (!currentServerModel && servers && servers.length > 0) {
					const firstId = servers[0].server_id
					setSelectedServerId(firstId)
					Cookies.set('selected_server', firstId)
				}
				if (selectedServerId) {
					refetchChannels()
				}
			})
		}
	}, [lastMessage, refetch, refetchChannels, selectedServerId, servers])

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

	useEffect(() => {
		if (isMounted.current && lastMessage) {
			refetchChat()
		}
	}, [lastMessage, refetchChat])

	useEffect(() => {
		if (selectedTextChannelId) {
			refetchChat()
		}
	}, [selectedTextChannelId, refetchChat])

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
							textChannels={textChannels}
							onTextChannelSelect={handleTextChannelSelect}
							selectedTextChannelId={selectedTextChannelId}
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
							<ProjectHeader
								projectName={currentServer?.name || ''}
								itemName={currentTextChannel?.name || ''}
							/>
						</div>
						<div
							style={{
								flex: 1,
								overflowY: 'auto',
								marginRight: '16px',
								minHeight: 0,
							}}
						>
							<ChatPanel
								chatData={
									chatItems?.map(item => ({
										name: item.user_data,
										text: item.text ?? '',
										// fileUrl: item.file_url,
									})) || []
								}
							/>
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

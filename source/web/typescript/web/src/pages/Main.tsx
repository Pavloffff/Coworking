import VoiceDevicesLogoPanel from '../components/panels/VoiceDevicesLogoPanel'
import InputPanel from '../components/panels/InputPanel'
import ProjectHeader from '../components/headers/ProjectHeader'
import ItemsPanel from '../components/panels/ItemsPanel'
import ChatPanel from '../components/panels/ChatPanel'
import { config } from '../config/config'
import { v4 as uuidv4 } from 'uuid'
import useWebSocket from 'react-use-websocket'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useQuery, useQueries } from '@tanstack/react-query'
import { serversApi } from '../api/servers/serversApi'
import Cookies from 'js-cookie'
import {
	ChatItemScheme,
	ServerModel,
	TextChannelModel,
	User,
	VoiceChannelModel,
	VoiceItemScheme,
} from '../api/types'
import { useNavigate } from 'react-router-dom'
import { textChannelsApi } from '../api/textChannels/textChannelsApi'
import { chatItemsApi } from '../api/chatItems/chatItemsApi'
import { userApi } from '../api/user/userApi'
import { voiceChannelsApi } from '../api/voiceChannels/voiceChannelsApi'
import { voiceItemsApi } from '../api/voiceItems/voiceItemsApi'

const Main = () => {
	const navigate = useNavigate()
	const [access_token, setAccessToken] = useState<string | null>(null)
	const [refresh_token, setRefreshToken] = useState<string | null>(null)

	useEffect(() => {
		// Синхронизация при монтировании
		const access = localStorage.getItem('access_token')
		const refresh = localStorage.getItem('refresh_token')

		if (access && refresh) {
			Cookies.set('access_token', access, { secure: true, sameSite: 'Lax' })
			Cookies.set('refresh_token', refresh, { secure: true, sameSite: 'Lax' })
			setAccessToken(access)
			setRefreshToken(refresh)
		} else {
			navigate('/login')
		}
	}, [navigate])

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
		localStorage.removeItem('access_token')
		localStorage.removeItem('refresh_token')
		Cookies.remove('access_token')
		Cookies.remove('refresh_token')
		navigate('/login')
		navigate('/')
	}, [navigate])

	const { data: servers, refetch } = useQuery<ServerModel[]>({
		queryKey: ['servers'],
		queryFn: async (): Promise<ServerModel[]> => {
			try {
				const response = await serversApi.getUserServers(
					access_token!,
					refresh_token!
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
				access_token!,
				refresh_token!
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

	const { data: voiceChannels, refetch: refetchVoiceChannels } = useQuery<
		VoiceChannelModel[]
	>({
		queryKey: ['voiceChannels', selectedServerId],
		queryFn: async () => {
			if (!selectedServerId) return []
			const response = await voiceChannelsApi.getServerVoiceChannels(
				parseInt(selectedServerId),
				access_token!,
				refresh_token!
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

	const { data: usersList, refetch: refetchUsers } = useQuery<User[]>({
		queryKey: ['usersList', selectedServerId],
		queryFn: async () => {
			if (!selectedServerId) return []
			const response = await userApi.getServerUsers(
				parseInt(selectedServerId),
				access_token!,
				refresh_token!
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

	const { data: currentServer, refetch: refetchServer } = useQuery({
		queryKey: ['currentServer', selectedServerId],
		queryFn: async () => {
			if (!selectedServerId) return null
			const response = await serversApi.getCurrentServer(
				parseInt(selectedServerId),
				access_token!,
				refresh_token!
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

	const { data: currentTextChannel, refetch: refetchTextChannel } = useQuery({
		queryKey: ['currentTextChannel', selectedTextChannelId],
		queryFn: async () => {
			if (!selectedTextChannelId) return null
			const response = await textChannelsApi.getCurrentTextChannel(
				parseInt(selectedTextChannelId),
				access_token!,
				refresh_token!
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

	const { data: currentUser, refetch: refetchUser } = useQuery({
		queryKey: ['currentUser'],
		queryFn: async () => {
			const response = await userApi.getCurrentUser(
				access_token!,
				refresh_token!
			)
			return response.data
		},
		refetchOnWindowFocus: false,
		refetchOnMount: false,
		refetchOnReconnect: false,
		staleTime: Infinity,
		retry: false,
		enabled: !!access_token,
	})

	const { data: chatItems, refetch: refetchChat } = useQuery<ChatItemScheme[]>({
		queryKey: ['chatItems', selectedTextChannelId],
		queryFn: async () => {
			if (!selectedTextChannelId) return []
			const response = await chatItemsApi.getTextChannelsChatItems(
				parseInt(selectedTextChannelId),
				access_token!,
				refresh_token!
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

	const voiceItemsQueries = useQueries({
		queries: (voiceChannels || []).map(channel => ({
			queryKey: ['voiceItems', channel.voice_channel_id],
			queryFn: async () => {
				const response = await voiceItemsApi.getVoiceChannelsVoiceItems(
					parseInt(channel.voice_channel_id),
					access_token!,
					refresh_token!
				)
				return response.data
			},
			enabled: !!voiceChannels && !!access_token,
		})),
	})

	const voiceItemsByChannel = useMemo(() => {
		const itemsByChannel: Record<string, VoiceItemScheme[]> = {}
		voiceChannels?.forEach((channel, index) => {
			const query = voiceItemsQueries[index]
			if (query.data) {
				itemsByChannel[channel.voice_channel_id] = query.data
			}
		})
		return itemsByChannel
	}, [voiceChannels, voiceItemsQueries])

	const [selectedVoiceChannelId, setSelectedVoiceChannelId] = useState<
		string | null
	>(null)
	const handleVoiceChannelSelect = useCallback(
		async (voiceChannelId: string) => {
			const currentUserId = currentUser?.user_id
			if (!currentUserId || !selectedServerId) return

			const serverId = parseInt(selectedServerId)
			const oldChannelId = selectedVoiceChannelId
			const newChannelId = voiceChannelId
			try {
				if (oldChannelId === newChannelId) {
					const currentItems = voiceItemsByChannel[newChannelId] || []
					const userItem = currentItems.find(i => i.user_id === currentUserId)

					if (userItem) {
						await voiceItemsApi.deleteVoiceItem(
							userItem.voice_item_id!,
							serverId,
							access_token!,
							refresh_token!
						)
						setSelectedVoiceChannelId(null)
						Cookies.remove('selected_voice_channel')
					} else {
						await voiceItemsApi.addVoiceItem(
							0,
							currentUserId,
							parseInt(newChannelId),
							access_token!,
							refresh_token!
						)
						setSelectedVoiceChannelId(newChannelId)
						Cookies.set('selected_voice_channel', newChannelId)
					}
				} else if (newChannelId) {
					if (oldChannelId) {
						const oldItems = voiceItemsByChannel[oldChannelId] || []
						const oldItem = oldItems.find(i => i.user_id === currentUserId)
						if (oldItem) {
							await voiceItemsApi.deleteVoiceItem(
								oldItem.voice_item_id!,
								serverId,
								access_token!,
								refresh_token!
							)
						}
					}

					await voiceItemsApi.addVoiceItem(
						0,
						currentUserId,
						parseInt(newChannelId),
						access_token!,
						refresh_token!
					)
					setSelectedVoiceChannelId(newChannelId)
					Cookies.set('selected_voice_channel', newChannelId)
				} else {
					if (oldChannelId) {
						const oldItems = voiceItemsByChannel[oldChannelId] || []
						const oldItem = oldItems.find(i => i.user_id === currentUserId)
						if (oldItem) {
							await voiceItemsApi.deleteVoiceItem(
								oldItem.voice_item_id!,
								serverId,
								access_token!,
								refresh_token!
							)
						}
					}
				}
				voiceItemsQueries.forEach(q => q.refetch())
			} catch (error) {
				console.error('Error handling voice channel:', error)
			}
		},
		[
			access_token,
			currentUser,
			refresh_token,
			selectedServerId,
			selectedVoiceChannelId,
			voiceItemsByChannel,
			voiceItemsQueries,
		]
	)

	const { data: currentVoiceChannel, refetch: refetchVoiceChannel } = useQuery({
		queryKey: ['currentVoiceChannel', selectedVoiceChannelId],
		queryFn: async () => {
			if (!selectedVoiceChannelId) return null
			const response = await voiceChannelsApi.getCurrentVoiceChannel(
				parseInt(selectedVoiceChannelId),
				access_token!,
				refresh_token!
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

	useEffect(() => {
		if (access_token) {
			wsUrl.current = `${
				config.notifications_pisher_ws_endpoint
			}/${uuidv4()}?token=${access_token}`
		}
	}, [access_token])

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
					refetchVoiceChannels()
					refetchUsers()
					refetchChat()
					voiceItemsQueries.map(q => q.refetch())
				}
			})
		}
	}, [
		lastMessage,
		refetch,
		refetchChannels,
		refetchVoiceChannels,
		refetchUsers,
		refetchChat,
		selectedServerId,
		voiceItemsQueries,
		servers,
	])

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
		if (access_token) {
			refetchUser()
		}
	}, [access_token, refetchUser])

	useEffect(() => {
		if (isMounted.current && lastMessage) {
			refetchChat()
		}
	}, [lastMessage, refetchChat])

	useEffect(() => {
		if (selectedServerId) {
			refetchServer()
		}
	}, [selectedServerId, refetchServer])

	useEffect(() => {
		if (selectedTextChannelId) {
			refetchTextChannel()
		}
	}, [selectedTextChannelId, refetchTextChannel])

	useEffect(() => {
		if (selectedVoiceChannelId) {
			refetchVoiceChannel()
		}
	}, [selectedVoiceChannelId, refetchVoiceChannel])

	useEffect(() => {
		if (selectedServerId) {
			refetchUsers()
		}
	}, [selectedServerId, refetchUsers])

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
							usersList={usersList}
							voiceChannels={voiceChannels}
							selectedVoiceChannelId={selectedVoiceChannelId}
							onVoiceChannelSelect={handleVoiceChannelSelect}
							voiceItemsByChannel={voiceItemsByChannel}
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
								itemName={currentTextChannel?.name || currentVoiceChannel?.name}
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
						<InputPanel
							currentUserId={currentUser?.user_id || 0}
							selectedTextChannelId={
								selectedTextChannelId ? parseInt(selectedTextChannelId) : null
							}
							refetchChat={refetchChat}
						/>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Main

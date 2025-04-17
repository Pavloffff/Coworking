import { useState, useEffect } from 'react'
import TabPanel from './TabPanel'
import ServersList from '../lists/ServersList'
import { ServerModel } from '../../api/types'
// import { serversApi } from '../../api/servers/serversApi'
// import { v4 as uuidv4 } from 'uuid'
// import { config } from '../../config/config'
// import Cookies from 'js-cookie'
// import { useQuery, useQueryClient } from '@tanstack/react-query'
// import useWebSocket from 'react-use-websocket'

// const useServers = () => {
// 	const queryClient = useQueryClient()
// 	const access_token = Cookies.get('access_token') as string

// 	// HTTP запрос с использованием React Query
// 	const {
// 		data: servers,
// 		isLoading,
// 		error,
// 	} = useQuery<ServerModel[]>({
// 		queryKey: ['servers'],
// 		queryFn: () =>
// 			serversApi.getUserServers(access_token).then(res => res.data),
// 		enabled: !!access_token,
// 		refetchOnMount: true,
// 	})

// 	// WebSocket подключение
// 	const { sendMessage } = useWebSocket(
// 		`${
// 			config.notifications_pisher_ws_endpoint
// 		}/${uuidv4()}?token=${access_token}`,
// 		{
// 			onMessage: () => {
// 				// Инвалидируем кэш при получении сообщения
// 				queryClient.invalidateQueries({ queryKey: ['servers'] })
// 			},
// 			shouldReconnect: () => true,
// 			reconnectAttempts: 10,
// 			reconnectInterval: 3000,
// 			onError: error => console.error('WebSocket error:', error),
// 			queryParams: { token: access_token },
// 		}
// 	)

// 	return { servers, isLoading, error, sendMessage }
// }

interface ItemsPanelProps {
	servers?: ServerModel[] | undefined 
	onServerSelect: (serverId: string) => void
	selectedServerId: string | null
  }

const ItemsPanel = ({
	servers,
	onServerSelect,
	selectedServerId 
}: ItemsPanelProps) => {
	const [selectedButton, setSelectedButton] = useState('btn1')
	const [dimensions, setDimensions] = useState({
		width: window.innerWidth,
		height: window.innerHeight,
	})
	// const { servers } = useServers()

	useEffect(() => {
		const handleResize = () => {
			setDimensions({
				width: window.innerWidth,
				height: window.innerHeight,
			})
		}
		window.addEventListener('resize', handleResize)
		return () => window.removeEventListener('resize', handleResize)
	}, [])
	const containerWidth = Math.min(dimensions.width - 32, 420)
	const containerHeight = (dimensions.height - 32) * 0.9

	// useEffect(() => {
	// 	console.log(Cookies.get('access_token'))
	// 	const token = Cookies.get('access_token') as string
	// 	const fetchServers = async () => {
	// 		try {
	// 			const response = await serversApi.getUserServers(token)
	// 			setServers(response.data)
	// 		} catch (error) {
	// 			console.error('Error fetching servers:', error)
	// 		}
	// 	}
	// 	const ws = new WebSocket(
	// 		`${
	// 			config.notifications_pisher_ws_endpoint
	// 		}/${uuidv4()}?token=${Cookies.get('access_token')}`
	// 	)
	// 	ws.onmessage = () => {
	// 		fetchServers()
	// 	}

	// 	// fetchServers()

	// 	return () => {}
	// })
	return (
		<div
			style={{
				display: 'flex',
				flexDirection: 'column',
				justifyContent: 'space-between',
				padding: '16px',
				boxSizing: 'border-box',
				width: containerWidth,
				height: containerHeight,
				border: '1px solid #e0e0e0',
				borderRadius: '8px',
				backgroundColor: '#f9f9f9',
				overflow: 'hidden',
			}}
		>
			<div
				style={{
					fontSize: '18px',
					fontWeight: 'bold',
					color: '#444',
					flexGrow: 1,
					overflowY: 'auto',
				}}
			>
				{selectedButton == 'btn1' ? (
					<ServersList
						data={servers || []}
						// data={mockServers}
						// isLoading={isLoading}
						// error={error?.message}
					/>
				) : selectedButton == 'btn2' ? (
					<div>
						{selectedServerId || -1}
					</div>
				) : (
					'234e234'
				)}
			</div>
			<div style={{ width: '100%' }}>
				<TabPanel
					selectedButton={selectedButton}
					onButtonSelect={setSelectedButton}
				/>
			</div>
		</div>
	)
}

export default ItemsPanel

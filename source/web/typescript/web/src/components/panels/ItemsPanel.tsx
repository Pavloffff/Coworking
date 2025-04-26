import { useState, useEffect } from 'react'
import TabPanel from './TabPanel'
import ServersList from '../lists/ServersList'
import {
	ServerModel,
	TextChannelModel,
	User,
	VoiceChannelModel,
	VoiceItemScheme,
} from '../../api/types'
import { Button, Input, Typography } from 'antd'
import { serversApi } from '../../api/servers/serversApi'
import Cookies from 'js-cookie'
import { textChannelsApi } from '../../api/textChannels/textChannelsApi'
import TextChannelsList from '../lists/TextChannelsList'
import UsersList from '../lists/UsersList'
import { userApi } from '../../api/user/userApi'
import { voiceChannelsApi } from '../../api/voiceChannels/voiceChannelsApi'
import VoiceChannelsList from '../lists/VoiceChannelsList'

interface ItemsPanelProps {
	servers?: ServerModel[] | undefined
	onServerSelect: (serverId: string) => void
	selectedServerId: string | null
	textChannels?: TextChannelModel[] | undefined
	onTextChannelSelect: (textChannelId: string) => void
	selectedTextChannelId: string | null
	usersList?: User[] | undefined
	voiceChannels?: VoiceChannelModel[] | undefined
	onVoiceChannelSelect: (voiceChannelId: string) => void
	selectedVoiceChannelId: string | null
	voiceItemsByChannel?: Record<string, VoiceItemScheme[]>
}

const ItemsPanel = ({
	servers,
	onServerSelect,
	selectedServerId,
	textChannels,
	onTextChannelSelect,
	selectedTextChannelId,
	usersList,
	voiceChannels,
	onVoiceChannelSelect,
	selectedVoiceChannelId,
	voiceItemsByChannel = {},
}: ItemsPanelProps) => {
	const [access_token, setAccessToken] = useState<string | null>(null)
	const [refresh_token, setRefreshToken] = useState<string | null>(null)
	useEffect(() => {
		const access = localStorage.getItem('access_token')
		const refresh = localStorage.getItem('refresh_token')

		if (access && refresh) {
			Cookies.set('access_token', access, { secure: true, sameSite: 'Lax' })
			Cookies.set('refresh_token', refresh, { secure: true, sameSite: 'Lax' })
			setAccessToken(access)
			setRefreshToken(refresh)
		}
	}, [])

	const [dimensions, setDimensions] = useState({
		width: window.innerWidth,
		height: window.innerHeight,
	})
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
	const containerWidth = Math.min(dimensions.width - 32, 460)
	const containerHeight = (dimensions.height - 32) * 0.9

	const [selectedButton, setSelectedButton] = useState('btn1')

	const [serverName, setServerName] = useState('')
	const handleAddServerClick = async () => {
		console.log('Введенное название сервера:', serverName)
		await serversApi.addServer(serverName, access_token!, refresh_token!)
		setServerName('')
	}

	const [textChannelName, setTextChannelName] = useState('')
	const handleAddTextChannelClick = async () => {
		console.log('Введенное название текстового канала:', textChannelName)
		await textChannelsApi.addTextChannel(
			(selectedServerId ?? '-1') as unknown as number,
			textChannelName,
			access_token!,
			refresh_token!
		)
		setTextChannelName('')
	}

	const [voiceChannelName, setVoiceChannelName] = useState('')
	const handleAddVoiceChannelClick = async () => {
		console.log('Введенное название голосового канала:', voiceChannelName)
		await voiceChannelsApi.addVoiceChannel(
			(selectedServerId ?? '-1') as unknown as number,
			voiceChannelName,
			access_token!,
			refresh_token!
		)
		setVoiceChannelName('')
	}

	const [serverUserData, setserverUserData] = useState('')
	const handleAddServerUserDataClick = async () => {
		console.log('Введенное имя участника:', serverUserData)
		await userApi.addServerUser(
			(selectedServerId ?? '-1') as unknown as number,
			serverUserData,
			access_token!,
			refresh_token!
		)
		setserverUserData('')
	}

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
				{selectedButton === 'btn1' ? (
					<div
						style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
					>
						<Typography.Title
							level={3}
							style={{ marginLeft: 10, marginBottom: 16 }}
						>
							Список серверов
						</Typography.Title>

						<div style={{ flex: 1, overflowY: 'auto' }}>
							<ServersList
								data={servers || []}
								selectedServerId={selectedServerId}
								onItemClick={onServerSelect}
							/>
						</div>
						<div
							style={{
								display: 'flex',
								gap: 8,
								marginBottom: 40,
								marginTop: 40,
								alignItems: 'center',
							}}
						>
							<Input
								placeholder="Создать сервер"
								style={{ flex: 1 }}
								size="large"
								value={serverName}
								onChange={e => setServerName(e.target.value)}
								onPressEnter={handleAddServerClick}
							/>
							<Button
								type="primary"
								style={{
									width: 40,
									height: 40,
									flexShrink: 0,
									fontSize: '18px',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
								onClick={handleAddServerClick}
							>
								+
							</Button>
						</div>
					</div>
				) : selectedButton === 'btn2' ? (
					<div
						style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
					>
						<div>
							<Typography.Title
								level={4}
								style={{ marginLeft: 10, marginBottom: 16 }}
							>
								Текстовые каналы
							</Typography.Title>
							<div style={{ flex: 1, overflowY: 'auto', maxHeight: '200px' }}>
								<TextChannelsList
									data={textChannels || []}
									selectedTextChannelId={selectedTextChannelId}
									onItemClick={onTextChannelSelect}
								/>
							</div>
							<div
								style={{
									display: 'flex',
									gap: 8,
									marginTop: 40,
									alignItems: 'center',
								}}
							>
								<Input
									placeholder="Создать текстовый канал"
									style={{ flex: 1 }}
									size="large"
									value={textChannelName}
									onChange={e => setTextChannelName(e.target.value)}
									onPressEnter={handleAddTextChannelClick}
								/>
								<Button
									type="primary"
									style={{
										width: 40,
										height: 40,
										flexShrink: 0,
										fontSize: '18px',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
									}}
									onClick={handleAddTextChannelClick}
								>
									+
								</Button>
							</div>
						</div>
						<div>
							<Typography.Title
								level={4}
								style={{ marginLeft: 10, marginBottom: 16 }}
							>
								Голосовые каналы
							</Typography.Title>
							<div style={{ flex: 1, overflowY: 'auto', maxHeight: '200px' }}>
								<VoiceChannelsList
									data={voiceChannels || []}
									selectedVoiceChannelId={selectedVoiceChannelId}
									onItemClick={onVoiceChannelSelect}
									voiceItemsByChannel={voiceItemsByChannel}
								/>
							</div>
							<div
								style={{
									display: 'flex',
									gap: 8,
									marginTop: 40,
									alignItems: 'center',
								}}
							>
								<Input
									placeholder="Создать голосовой канал"
									style={{ flex: 1 }}
									size="large"
									value={voiceChannelName}
									onChange={e => setVoiceChannelName(e.target.value)}
									onPressEnter={handleAddVoiceChannelClick}
								/>
								<Button
									type="primary"
									style={{
										width: 40,
										height: 40,
										flexShrink: 0,
										fontSize: '18px',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
									}}
									onClick={handleAddVoiceChannelClick}
								>
									+
								</Button>
							</div>
						</div>
					</div>
				) : selectedButton === 'btn3' ? (
					<div
						style={{
							display: 'flex',
							flexDirection: 'column',
							height: '100%',
						}}
					>
						<div
							style={{
								display: 'flex',
								flexDirection: 'column',
								height: '100%',
							}}
						>
							<Typography.Title
								level={3}
								style={{ marginLeft: 10, marginBottom: 16 }}
							>
								Участники сервера
							</Typography.Title>
							<UsersList
								data={
									usersList?.map(item => ({
										email: item.email,
										name: item.name,
										avatar_url: item.avatar_url,
										tag: (item.tag ?? 0).toString(),
										user_id: (item.user_id ?? 0).toString(),
									})) || []
								}
							/>
						</div>
						<div
							style={{
								display: 'flex',
								gap: 8,
								marginTop: 40,
								marginBottom: 40,
								alignItems: 'center',
							}}
						>
							<Input
								placeholder="Пригласить участника"
								style={{ flex: 1 }}
								size="large"
								value={serverUserData}
								onChange={e => setserverUserData(e.target.value)}
								onPressEnter={handleAddServerUserDataClick}
							/>
							<Button
								type="primary"
								style={{
									width: 40,
									height: 40,
									flexShrink: 0,
									fontSize: '18px',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
								onClick={handleAddServerUserDataClick}
							>
								+
							</Button>
						</div>
					</div>
				) : (
					<Typography.Title
						level={3}
						style={{ marginLeft: 10, marginBottom: 16 }}
					>
						Настройки
					</Typography.Title>
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

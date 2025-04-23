import { List } from 'antd'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'

interface VoiceChannelItem {
	voice_channel_id: string
	name: string
	server_id: number
}

interface VoiceChannelsListProps {
	data: VoiceChannelItem[]
	selectedVoiceChannelId?: string | null
	onItemClick?: (textChannelId: string) => void
}

const VoiceChannelsList = ({
	data,
	selectedVoiceChannelId,
	onItemClick,
}: VoiceChannelsListProps) => {
	const [internalSelectedId, setInternalSelectedId] = useState<string | null>(
		() =>
			Cookies.get('selected_voice_channel_id') ||
			(data[0]?.voice_channel_id ?? '')
	)

	useEffect(() => {
		if (selectedVoiceChannelId !== undefined) {
			setInternalSelectedId(selectedVoiceChannelId)
		}
	}, [selectedVoiceChannelId])

	const handleVoiceChannelClick = (textChannel: VoiceChannelItem) => {
		const newId =
			internalSelectedId === textChannel.voice_channel_id
				? ''
				: textChannel.voice_channel_id
		setInternalSelectedId(newId)
		onItemClick?.(newId)
		Cookies.set('selected_voice_channel_id', newId)
	}
	return (
		<List
			style={{
				height: '200px',
			}}
			itemLayout="horizontal"
			dataSource={data}
			renderItem={item => (
				<List.Item
					key={item.server_id}
					onClick={() => handleVoiceChannelClick(item)}
					style={{
						cursor: 'pointer',
						padding: '12px 16px',
						borderBottom: '1px solid #f0f0f0',
						backgroundColor:
							item.voice_channel_id === internalSelectedId
								? '#f5f5f5'
								: 'white',
						transition: 'background-color 0.2s',
					}}
				>
					<List.Item.Meta
						title={
							<span
								style={{
									fontWeight: 500,
									fontSize: '15px',
									color: '#333',
									whiteSpace: 'nowrap',
									overflow: 'hidden',
									textOverflow: 'ellipsis',
									maxWidth: 'calc(100% - 48px)',
								}}
							>
								{item.name}
							</span>
						}
					/>
				</List.Item>
			)}
		/>
	)
}

export default VoiceChannelsList

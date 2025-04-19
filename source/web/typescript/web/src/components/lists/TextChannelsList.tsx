import { List } from 'antd'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'

interface TextChannelItem {
	text_channel_id: string
	name: string
	server_id: number
}

interface TextChannelsListProps {
	data: TextChannelItem[]
	selectedTextChannelId?: string | null
	onItemClick?: (textChannelId: string) => void
}

const TextChannelsList = ({
	data,
	selectedTextChannelId,
	onItemClick,
}: TextChannelsListProps) => {
	const [internalSelectedId, setInternalSelectedId] = useState<string | null>(
		() =>
			Cookies.get('selected_text_channel_id') ||
			(data[0]?.text_channel_id ?? '')
	)

	useEffect(() => {
		if (selectedTextChannelId !== undefined) {
			setInternalSelectedId(selectedTextChannelId)
		}
	}, [selectedTextChannelId])

	const handleTextChannelClick = (textChannel: TextChannelItem) => {
		const newId =
			internalSelectedId === textChannel.text_channel_id
				? ''
				: textChannel.text_channel_id
		setInternalSelectedId(newId)
		onItemClick?.(newId)
		Cookies.set('selected_text_channel_id', newId)
	}
	return (
		<List
			itemLayout="horizontal"
			dataSource={data}
			renderItem={item => (
				<List.Item
					key={item.server_id}
					onClick={() => handleTextChannelClick(item)}
					style={{
						cursor: 'pointer',
						padding: '12px 16px',
						borderBottom: '1px solid #f0f0f0',
						backgroundColor:
							item.text_channel_id === internalSelectedId ? '#f5f5f5' : 'white',
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

export default TextChannelsList

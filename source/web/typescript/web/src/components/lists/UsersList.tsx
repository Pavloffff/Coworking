import { List, Avatar } from 'antd'

interface UserItem {
	user_id: string
	email: string
	name: string
	tag: string
	avatar_url?: string
}

interface UsersListProps {
	data: UserItem[]
}

const UsersList = ({ data }: UsersListProps) => {
	return (
		<List
			itemLayout="horizontal"
			dataSource={data}
			renderItem={item => (
				<List.Item
					key={item.user_id}
					style={{
						cursor: 'pointer',
						padding: '12px 16px',
						borderBottom: '1px solid #f0f0f0',
						backgroundColor: 'white',
						transition: 'background-color 0.2s',
					}}
				>
					<List.Item.Meta
						avatar={
							<Avatar
								src={item.avatar_url}
								style={{
									backgroundColor: item.avatar_url ? 'transparent' : '#f0f0f0',
									border: '1px solid #e8e8e8',
								}}
							>
								{!item.avatar_url && ' '}
							</Avatar>
						}
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
								{item.name}#
								{String((parseInt(item.tag) || 0) % 10000).padStart(4, '0')}
							</span>
						}
					/>
				</List.Item>
			)}
		/>
	)
}

export default UsersList

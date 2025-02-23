import React from 'react'
import { Typography } from 'antd'

interface ProjectHeaderProps {
	projectName: string
	itemName?: string
}
const { Title } = Typography

const ProjectHeader: React.FC<ProjectHeaderProps> = ({
	projectName,
	itemName,
}) => {
	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				gap: '8px',
				marginLeft: '8px',
				marginRight: '12px',
			}}
		>
			<Title level={2} style={{ margin: 0 }}>
				{projectName}
			</Title>
			<Title level={3} style={{ margin: 0 }}>
				- {itemName ? itemName : ''}
			</Title>
		</div>
	)
}

export default ProjectHeader

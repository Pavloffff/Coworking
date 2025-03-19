import { useState, useEffect } from 'react'
import TabPanel from './TabPanel'
import { Typography } from 'antd'
import SubmenuList from '../lists/SubmenuList'

const { Title } = Typography

const ItemsPanel = () => {
	const [selectedButton, setSelectedButton] = useState('btn1')
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

	const containerWidth = Math.min(dimensions.width - 32, 465)
	const containerHeight = (dimensions.height - 32) * 0.9

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
				}}
			>
				{selectedButton == 'btn1' ? (
					<div>
						<SubmenuList title="Переписки" />
					</div>
				) : (
					'2143324'
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

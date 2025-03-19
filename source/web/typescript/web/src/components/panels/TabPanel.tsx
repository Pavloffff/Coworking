import GreyButton from '../buttons/GreyButton'
import ButtonCollection from '../collections/ButtonCollection'
import {
	MenuOutlined,
	OrderedListOutlined,
	TeamOutlined,
	UserOutlined,
} from '@ant-design/icons'

interface TabPanelProps {
	selectedButton: string
	onButtonSelect: (buttonKey: string) => void
}

const TabPanel: React.FC<TabPanelProps> = ({
	selectedButton,
	onButtonSelect,
}) => {
	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-between',
				width: '100%',
			}}
		>
			<ButtonCollection
				buttons={[
					<GreyButton
						key="btn1"
						icon={<OrderedListOutlined />}
						shade={selectedButton === 'btn1' ? '#444' : '#ccc'}
						onClick={() => onButtonSelect('btn1')}
					/>,
					<GreyButton
						key="btn2"
						icon={<MenuOutlined />}
						shade={selectedButton === 'btn2' ? '#444' : '#ccc'}
						onClick={() => onButtonSelect('btn2')}
					/>,
					<GreyButton
						key="btn3"
						icon={<TeamOutlined />}
						shade={selectedButton === 'btn3' ? '#444' : '#ccc'}
						onClick={() => onButtonSelect('btn3')}
					/>,
				]}
				align="16px"
			/>

			<GreyButton
				key="rightBtn"
				icon={<UserOutlined />}
				shade={selectedButton === 'rightBtn' ? '#444' : '#ccc'}
				onClick={() => onButtonSelect('rightBtn')}
				style={{ marginLeft: 'auto' }}
			/>
		</div>
	)
}

export default TabPanel

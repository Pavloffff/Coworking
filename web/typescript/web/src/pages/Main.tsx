import VoiceDevicesLogoPanel from '../components/panels/VoiceDevicesLogoPanel'
import InputPanel from '../components/panels/InputPanel'
import ProjectHeader from '../components/headers/ProjectHeader'
import ItemsPanel from '../components/panels/ItemsPanel'
import ChatPanel from '../components/panels/ChatPanel'

const chatData = [
	{
		name: 'Иван Иванов',
		text: 'Привет! Как дела?',
	},
	{
		name: 'Мария Петрова',
		text: 'Привет! Пока не родила!',
	},
	{
		name: 'Пидр Сидоров',
		text: 'Как продвигается проект?',
	},
	{
		name: 'Анна Кузнецова',
		text: 'Мы почти готовы!',
	},
	{
		name: 'Иван Иванов',
		text: 'Привет! Как дела?',
	},
	{
		name: 'Мария Петрова',
		text: 'Привет! Пока не родила!',
	},
	{
		name: 'Пидр Сидоров',
		text: 'Как продвигается проект?',
	},
	{
		name: 'Анна Кузнецова',
		text: 'Мы почти готовы!',
	},
]

const Main = () => {
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
						<ItemsPanel />
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
							<ProjectHeader projectName="Dungeon" itemName="чат Пивальди" />
						</div>
						<div
							style={{
								flex: 1,
								overflowY: 'auto',
								marginRight: '16px',
								minHeight: 0,
							}}
						>
							<ChatPanel chatData={chatData} />
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

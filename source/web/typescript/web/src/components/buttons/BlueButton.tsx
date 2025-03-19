import { Button, ButtonProps } from 'antd'

interface BlueButtonProps extends ButtonProps {
	icon?: React.ReactNode
}

const BlueButton = (props: BlueButtonProps) => {
	const { icon, ...restProps } = props

	return (
		<Button
			{...restProps}
			type="primary"
			icon={icon}
			style={{
				width: '58px',
				height: '58px',
				borderRadius: '10px',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
			}}
		></Button>
	)
}

export default BlueButton

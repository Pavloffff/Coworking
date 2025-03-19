import { Button, ButtonProps } from 'antd'
import React from 'react'

interface GreyButtonProps extends ButtonProps {
	icon?: React.ReactNode
	shade?: string
}

const GreyButton = (props: GreyButtonProps) => {
	const { icon, shade = '#ccc', ...restProps } = props

	return (
		<Button
			{...restProps}
			type="default"
			icon={icon}
			style={{
				width: '64px',
				height: '64px',
				borderRadius: '50%',
				backgroundColor: shade,
				border: 'none',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
			}}
		></Button>
	)
}

export default GreyButton

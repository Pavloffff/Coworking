import React from 'react'

interface ButtonCollectionProps {
	buttons: React.ReactNode[]
	align?: string
}

const ButtonCollection: React.FC<ButtonCollectionProps> = ({
	buttons,
	align = '16px',
}) => {
	return (
		<div
			style={{
				display: 'flex',
				gap: align,
			}}
		>
			{buttons.map((button, index) => (
				<div key={index} style={{ margin: 0 }}>
					{button}
				</div>
			))}
		</div>
	)
}

export default ButtonCollection

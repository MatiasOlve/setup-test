import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'TODO: Update title',
  description: ''
}

const RootLayout = ({
  children
}: Readonly<{
  children: React.ReactNode
}>) => {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

export default RootLayout

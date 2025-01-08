import { NextRequest, NextResponse } from 'next/server'

const USERNAME = process.env.USERNAME
const PASSWORD = process.env.PASSWORD
const IS_PROTECTED = process.env.PROTECTED === 'true'

// Define a type for the session data
interface SessionDataInterface {
  expiry: number
  // Add any other session-related properties here
}

// Define the type for the session store
const sessionStore: Record<string, SessionDataInterface> = {}

const isValidSession = (sessionToken: string) => {
  const session = sessionStore[sessionToken]

  if (!session) {
    return false
  }

  //   Check if the session has expired
  const now = new Date().getTime()

  if (now > session.expiry) {
    // Optionally, clean up by deleting the expired session
    delete sessionStore[sessionToken]
    return false
  }

  return true
}

const generateSessionToken = () => {
  // Create a new Uint8Array to hold the random values
  const array = new Uint8Array(32)
  // Fill the array with random values
  crypto.getRandomValues(array)

  // Convert the array to a hex string

  const token = Array.from(array, (byte) =>
    byte.toString(16).padStart(2, '0')
  ).join('')

  const expiry = new Date().getTime() + 24 * 60 * 60 * 1000 // 24 hours from now

  // Store the token with its expiry
  sessionStore[token] = { expiry }

  return token
}

export const middleware = (request: NextRequest) => {
  if (!IS_PROTECTED) {
    return NextResponse.next()
  }

  // Check if the session is already validated
  const session = request.cookies.get('session_token')

  if (session) {
    // Validate the session (you need to implement this part)
    if (isValidSession(session.value)) {
      return NextResponse.next()
    }
  }

  // Check for basic auth header
  const auth = request.headers.get('authorization')

  if (!auth) {
    return new Response('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Secure Area"'
      }
    })
  }

  // Verify the auth header.
  const expectedAuth = `Basic ${btoa(`${USERNAME}:${PASSWORD}`)}`

  if (expectedAuth === auth) {
    // Set a session token in the cookie
    const response = NextResponse.next()

    response.cookies.set('session_token', generateSessionToken(), {
      httpOnly: true,
      sameSite: 'strict'
    })

    return response
  }

  return new Response('Invalid credentials', { status: 401 })
}
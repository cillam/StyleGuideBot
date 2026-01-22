import ChatContainer from './components/ChatContainer';

function App() {
  return (
    <div className="flex flex-col h-screen">
      <ChatContainer />
      <footer className="text-center text-xs text-gray-500 py-3 border-t">
        This site is protected by reCAPTCHA and the Google{' '}
        <a 
          href="https://policies.google.com/privacy"
          className="text-blue-600 hover:underline"
        >
          Privacy Policy
        </a>{' '}
        and{' '}
        <a 
          href="https://policies.google.com/terms"
          className="text-blue-600 hover:underline"
        >
          Terms of Service
        </a>{' '}
        apply.
      </footer>
    </div>
  );
}

export default App;
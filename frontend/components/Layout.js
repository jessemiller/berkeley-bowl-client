import Link from 'next/link';
import { useRouter } from 'next/router';
import { clearSession, getSessionId } from '../lib/api';

export default function Layout({ children }) {
  const router = useRouter();
  const sessionId = getSessionId();

  const handleLogout = () => {
    clearSession();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/search" className="text-xl font-bold text-green-700">
                🥬 Berkeley Bowl
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              {sessionId && (
                <>
                  <Link
                    href="/search"
                    className="text-gray-700 hover:text-green-700 px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Search
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Logout
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}


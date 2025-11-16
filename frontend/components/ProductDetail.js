import { useState } from 'react';
import { useRouter } from 'next/router';
import { addToCart } from '../lib/api';

export default function ProductDetail({ product }) {
  const router = useRouter();
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const price = product.price || product.salePrice || 'N/A';
  const imageUrl = product.imageUrl || product.thumbnailUrl || null;
  const storeProductId = product.id || product.storeProductId;

  const handleAddToCart = async () => {
    if (!storeProductId) {
      setMessage('Error: Product ID not found');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await addToCart(storeProductId, quantity, 'each');
      setMessage('✅ Item added to cart successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage(`Error: ${err.response?.data?.detail || err.message || 'Failed to add to cart'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={() => router.back()}
        className="mb-4 text-green-600 hover:text-green-700 font-medium"
      >
        ← Back to search
      </button>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="md:flex">
          <div className="md:w-1/2">
            {imageUrl ? (
              <img
                src={imageUrl}
                alt={product.title}
                className="w-full h-96 object-cover"
              />
            ) : (
              <div className="w-full h-96 bg-gray-200 flex items-center justify-center text-gray-400">
                No Image Available
              </div>
            )}
          </div>
          <div className="md:w-1/2 p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-4">
              {product.title}
            </h1>

            <div className="mb-6">
              <p className="text-4xl font-bold text-green-600 mb-2">
                {typeof price === 'number' ? `$${price.toFixed(2)}` : price}
              </p>
              {product.unit && (
                <p className="text-gray-600">{product.unit}</p>
              )}
            </div>

            {product.description && (
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Description</h2>
                <p className="text-gray-700">{product.description}</p>
              </div>
            )}

            {product.sku && (
              <div className="mb-6">
                <p className="text-sm text-gray-500">SKU: {product.sku}</p>
              </div>
            )}

            <div className="border-t pt-6">
              <div className="flex items-center gap-4 mb-4">
                <label htmlFor="quantity" className="font-semibold">
                  Quantity:
                </label>
                <input
                  id="quantity"
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                  className="w-20 border rounded px-3 py-2 text-center"
                />
              </div>

              {message && (
                <div
                  className={`mb-4 p-3 rounded ${
                    message.includes('Error')
                      ? 'bg-red-100 text-red-700'
                      : 'bg-green-100 text-green-700'
                  }`}
                >
                  {message}
                </div>
              )}

              <button
                onClick={handleAddToCart}
                disabled={loading || !storeProductId}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Adding to cart...' : 'Add to Cart'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {process.env.NODE_ENV === 'development' && (
        <div className="mt-8 bg-gray-100 p-4 rounded text-xs overflow-auto">
          <pre>{JSON.stringify(product, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}


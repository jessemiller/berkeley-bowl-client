import { useRouter } from 'next/router';

export default function ProductCard({ product }) {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/product/${product.upc}`);
  };

  const price = product.price || product.salePrice || 'N/A';
  const imageUrl = product.thumbImage || '/placeholder.png';

  return (
    <div
      onClick={handleClick}
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
    >
      <div className="aspect-w-1 aspect-h-1 bg-gray-200">
        {imageUrl && imageUrl !== '/placeholder.png' ? (
          <img
            src={imageUrl}
            alt={product.title}
            className="w-full h-48 object-cover"
          />
        ) : (
          <div className="w-full h-48 flex items-center justify-center text-gray-400">
            No Image
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">
          {product.title} {product.id}
        </h3>
        <p className="text-green-600 font-bold text-lg">
          {typeof price === 'number' ? `$${price.toFixed(2)}` : price}
        </p>
        {product.unit && (
          <p className="text-sm text-gray-500 mt-1">{product.unit}</p>
        )}
      </div>
    </div>
  );
}


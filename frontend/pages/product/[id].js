import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import ProductDetail from '../../components/ProductDetail';
import { getProduct, getSessionId } from '../../lib/api';

export default function ProductPage() {
  const router = useRouter();
  const { id } = router.query;
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Redirect to login if not authenticated
    if (!getSessionId() && typeof window !== 'undefined') {
      router.push('/');
      return;
    }

    if (id) {
      loadProduct();
    }
  }, [id, router]);

  const loadProduct = async () => {
    setLoading(true);
    setError('');

    try {
      const result = await getProduct(id);
      setProduct(result?.data || result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load product');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </Layout>
    );
  }

  if (!product) {
    return (
      <Layout>
        <div className="text-center py-12 text-gray-500">Product not found</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <ProductDetail product={product} />
    </Layout>
  );
}


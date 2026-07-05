import { useState } from 'react';
import type { SubmitEventHandler } from 'react';
import { Link, useLoaderData, useNavigate, useSearchParams } from 'react-router-dom'
import { API_URL } from '../globals';

export default function Search() {
    const products = useLoaderData() as any[];
    const [searchParams, setSearchParams] = useSearchParams();

    const [inputValue, setInputValue] = useState(searchParams.get('q') || '');

    const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (inputValue.trim()) {
            setSearchParams({ q: inputValue.trim() });
        } else {
            setSearchParams({});
        }
    };
    return (
        <div style={{ padding: '20px' }}>
            <h2>Product Search</h2>

            {/* Internal Search Input */}
            <div style={{ marginBottom: '20px' }}>
                <form onSubmit={handleSearchSubmit} style={{ marginBottom: '20px', display: 'flex', gap: '8px' }}>
                    <input
                        type="text"
                        placeholder="Search for items..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)} // Just updates local state, doesn't search yet
                        style={{ padding: '8px 12px', width: '300px', borderRadius: '4px', border: '1px solid #ccc' }}
                    />
                    <button type="submit" style={{ padding: '8px 16px', cursor: 'pointer' }}>
                        Search
                    </button>
                </form>
            </div>

            <hr style={{ margin: '20px 0', borderColor: '#eee' }} />

            {/* Search Results Matrix */}
            <div style={{ display: 'grid', gap: '16px' }}>
                {products.length > 0 ? (
                    products.map((product) => (
                        <div key={product.id} style={{ border: '1px solid #eee', padding: '12px', borderRadius: '4px' }}>
                            <h3>{product.name}</h3>
                            <p>${product.price}</p>
                            <Link to={`/products/${product.id}`}>View Product</Link>
                        </div>
                    ))
                ) : (
                    searchParams.get('q') && <p>No products found matching "{searchParams.get('q')}"</p>
                )}
            </div>
        </div>
    );
}

export async function searchLoader({ request }: { request: Request }) {
    const url = new URL(request.url);
    const q = url.searchParams.get('q') || '';

    if (!q) return [];

    const response = await fetch(`${API_URL}products/?name=${encodeURIComponent(q)}`);
    if (response.status === 404) {
        return [];
    }
    if (!response.ok) throw new Response("Failed to search", { status: response.status });

    return response.json()
}
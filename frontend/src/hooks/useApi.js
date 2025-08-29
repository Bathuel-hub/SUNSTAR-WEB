import { useState, useEffect } from 'react';
import { api } from '../services/api';

export const useCompanyInfo = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.getCompanyInfo();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch company info:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};

export const useProductCategories = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.getProductCategories();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch product categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};

export const useTestimonials = (featuredOnly = true) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.getTestimonials(featuredOnly);
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch testimonials:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [featuredOnly]);

  return { data, loading, error };
};

export const useAdvantages = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await api.getAdvantages();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch advantages:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};
export interface UserProfile {
  email: string;
  name?: string;
  password?: string;
}

export interface RecipeSuggestion extends Recipe {
  recommendation_key: string;
  matched_ingredients?: string[];
  missing_ingredients?: string[];
}

export interface Recipe {
  id?: number;
  meal_id: string;
  title: string;
  description?: string;
  image_url: string;
  isMealPrepRecipe: boolean;
  time_minutes: number;
  price_level: number;
  tags?: { id?: number; name: string }[];
  ingredients?: Ingredient[];
  instructions: string;
  nutritionalInfo: Record<string, unknown>;
  match_score?: number;
  matching_ingredients?: number;
}

export interface Ingredient {
  id?: number;
  label: string;
  amount: string;
  unit: string;
  category?: string;
}

export interface Tag {
  id?: number;
  name: string;
}

export interface Meal {
  id?: number;
  meal_id: string;
  name: string;
}

export interface MealPlan {
  id?: number;
  meal_plan_id: string;
  client_name: string;
  client_weight: number;
  client_height: number;
  plan_type: string;
  plan_length_in_weeks: number;
  current_week: number;
  tracking_days: string[];
  prep_day: string;
  daily_goals: Record<string, unknown>;
  meals_per_day: Record<string, unknown>;
  meals: Record<string, unknown>;
}

export interface FoodProduct {
  id: number;
  barcode: string;
  name: string;
  brand: string;
  image_url: string;
  calories_100g: number | null;
  protein_100g: number | null;
  carbohydrates_100g: number | null;
  fat_100g: number | null;
  sugars_100g: number | null;
  nutriscore: string;
  fetched_at: string;
  source_url: string;
}

export interface FoodSummary {
  count: number;
  average_calories: number | null;
  average_protein: number | null;
}

export interface UserProfile {
  email: string;
  name?: string;
  password?: string;
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
}

export interface Ingredient {
  id?: number;
  label: string;
  amount: string;
  unit: string;
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

"""
Example usage of the Anomaly Score Organizer

This script demonstrates how to:
1. Use smart batch creator to organize images
2. Run predictions with predict_system
3. Organize images into folders based on anomaly scores with customizable thresholds
"""

from pathlib import Path
from vision_ad_tool.inference.anomaly_score_organizer import (
    predict_and_organize_by_score,
    organize_images_by_score
)

# =============================================================================
# EXAMPLE 1: Simple Two-Folder Organization (Normal vs Anomaly)
# =============================================================================

def example_simple_two_folders():
    """
    Organize images into two folders based on anomaly score:
    - Folder "0.5": Images with score <= 0.5 (likely normal)
    - Folder "1.0": Images with score > 0.5 (likely anomalies)
    """
    results = predict_and_organize_by_score(
        model_path="path/to/your/model.ckpt",  # Your trained model
        image_list_file="path/to/images.txt",   # Text file with image paths
        output_dir="organized_output_simple",
        score_thresholds=[0.5, 1.0],  # Two folders only
        copy_mode=True,  # Copy files (keep originals)
        save_metadata=True  # Save JSON metadata for each folder
    )

    print("\n📊 Results:")
    print(f"Organization stats: {results['organization_stats']}")


# =============================================================================
# EXAMPLE 2: Fine-Grained Organization with 8 Folders
# =============================================================================

def example_fine_grained_organization():
    """
    Organize images into 8 folders for detailed score distribution:
    - 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
    """
    results = predict_and_organize_by_score(
        model_path="path/to/your/model.ckpt",
        image_list_file="path/to/images.txt",
        output_dir="organized_output_detailed",
        score_thresholds=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        copy_mode=True,
        save_heatmap=True,  # Also save heatmap visualizations
        heatmap_style="side_by_side"  # Show original and heatmap side-by-side
    )

    # Access folder statistics
    folder_stats = results['organization_stats']['folder_stats']

    print("\n📊 Detailed Statistics:")
    for threshold, stats in folder_stats.items():
        print(f"Folder {threshold}: {stats['count']} images, "
              f"avg score: {stats['avg_score']:.4f}")


# =============================================================================
# EXAMPLE 3: Custom Thresholds (e.g., Quality Control Categories)
# =============================================================================

def example_custom_thresholds():
    """
    Custom organization for quality control:
    - 0.25: Excellent quality
    - 0.5: Good quality
    - 0.75: Needs review
    - 1.0: Defect/Anomaly
    """
    results = predict_and_organize_by_score(
        model_path="path/to/your/model.ckpt",
        image_list_file="path/to/images.txt",
        output_dir="organized_output_qc",
        score_thresholds=[0.25, 0.5, 0.75, 1.0],
        copy_mode=False,  # Move files instead of copying
        batch_id="quality_control_batch_001"
    )

    return results


# =============================================================================
# EXAMPLE 4: Organize Already-Predicted Results
# =============================================================================

def example_organize_existing_results():
    """
    If you already have prediction results, you can organize them directly
    without running predictions again.
    """
    # Assume you already have prediction results from a previous run
    from vision_ad_tool.inference.prediction_system import predict_image_list_from_file_enhanced

    # Step 1: Get predictions
    prediction_output = predict_image_list_from_file_enhanced(
        model_path="path/to/your/model.ckpt",
        image_list_file="path/to/images.txt",
        batch_id="batch_001",
        output_dir="predictions_only",
        save_results=True
    )

    # Step 2: Organize the results with different threshold sets
    # Try multiple threshold configurations on the same results

    # Configuration A: Simple binary classification
    stats_binary = organize_images_by_score(
        prediction_results=prediction_output['results'],
        output_dir="organized_binary",
        score_thresholds=[0.5, 1.0],
        copy_mode=True
    )

    # Configuration B: Detailed distribution
    stats_detailed = organize_images_by_score(
        prediction_results=prediction_output['results'],
        output_dir="organized_detailed",
        score_thresholds=[0.2, 0.4, 0.6, 0.8, 1.0],
        copy_mode=True
    )

    return stats_binary, stats_detailed


# =============================================================================
# EXAMPLE 5: Batch Processing with Smart Batch Creator
# =============================================================================

def example_batch_processing():
    """
    Process images in batches using the smart batch creator
    """
    from vision_ad_tool.inference.multinode_inference import (
        scan_folder_structure,
        create_smart_batches,
        create_batch_list_file
    )

    # Step 1: Scan folder structure
    folder_info = scan_folder_structure(Path("path/to/image/folder"))

    # Step 2: Create smart batches
    batches = create_smart_batches(folder_info, batch_size=100)

    print(f"Created {len(batches)} batches")

    # Step 3: Process each batch and organize by score
    for i, batch in enumerate(batches):
        batch_list_file = Path(f"batch_{i:04d}_images.txt")
        create_batch_list_file(batch, batch_list_file)

        results = predict_and_organize_by_score(
            model_path="path/to/your/model.ckpt",
            image_list_file=batch_list_file,
            output_dir=f"organized_batch_{i:04d}",
            score_thresholds=[0.3, 0.5, 0.7, 1.0],
            batch_id=f"batch_{i:04d}",
            copy_mode=True
        )

        print(f"Batch {i}: Organized {results['organization_stats']['total_processed']} images")


# =============================================================================
# EXAMPLE 6: Understanding the Output Structure
# =============================================================================

def example_output_structure():
    """
    Understanding the output directory structure and metadata
    """
    # After running predict_and_organize_by_score, you get:

    # Directory structure:
    # organized_output/
    # ├── 0.3/
    # │   ├── image1.jpg
    # │   ├── image2.jpg
    # │   └── metadata.json
    # ├── 0.5/
    # │   ├── image3.jpg
    # │   └── metadata.json
    # ├── 0.7/
    # │   ├── image4.jpg
    # │   └── metadata.json
    # └── 1.0/
    #     ├── image5.jpg
    #     └── metadata.json

    # Each metadata.json contains:
    # {
    #   "threshold": "0.5",
    #   "count": 10,
    #   "avg_score": 0.45,
    #   "min_score": 0.31,
    #   "max_score": 0.50,
    #   "images": ["path/to/image1.jpg", ...]
    # }

    # Reading metadata
    import json

    metadata_path = Path("organized_output/0.5/metadata.json")
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            print(f"\nFolder 0.5 statistics:")
            print(f"  Images: {metadata['count']}")
            print(f"  Average score: {metadata['avg_score']:.4f}")
            print(f"  Score range: [{metadata['min_score']:.4f}, {metadata['max_score']:.4f}]")


if __name__ == "__main__":
    print("Anomaly Score Organizer Examples")
    print("=" * 70)
    print("\nThese are example functions. Uncomment the one you want to run:")
    print("1. example_simple_two_folders() - Simple binary organization")
    print("2. example_fine_grained_organization() - Detailed 8-folder organization")
    print("3. example_custom_thresholds() - Custom QC categories")
    print("4. example_organize_existing_results() - Organize already-predicted results")
    print("5. example_batch_processing() - Batch processing with smart batches")
    print("6. example_output_structure() - Understanding the output")

    # Uncomment the example you want to run:
    # example_simple_two_folders()
    # example_fine_grained_organization()
    # example_custom_thresholds()
    # example_organize_existing_results()
    # example_batch_processing()
    # example_output_structure()
